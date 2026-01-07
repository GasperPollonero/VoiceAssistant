from dataclasses import dataclass
from typing import Any, Sequence # Sequence is a generic type for every type that behaves like a list (es. list, tuple, etc.)
from intent_ml import predict_intent
from actions import handle_action
import re
from text_to_num import alpha2digit

@dataclass
class NlpResult:
    reply_text : str
    action : str | None = None
    params : dict[str, Any] | None = None
    
def get_response(user_text: str, user_id : str | None = None, history: Sequence[str] | None = None) -> NlpResult:
    
    user_text = user_text.lower()
    intent, prob = predict_intent(user_text)
    
    if user_text.find("camera") != -1:
        return NlpResult("", action="camera", params=["status"])
    
    match intent:
        
        case "greeting":
            return NlpResult("buongiorno a te!")
        
        case "goodbye":
            return NlpResult("arrivederci!")
        
        case "set_volume":
            
            # convert text numbers in digits.
            text = alpha2digit(user_text, "it")
            
            # search for numbers.
            m = re.search(r"\b(\d{1,3})\b", text)
            if m:
                volume = int(m.group(1))
                print("volume: ", volume)
            else:
                # check for 'zero'
                m = re.search(r"\b(zero)\b", text)
                if m:
                    volume = 0
                else:
                    return NlpResult("Specifica il volume.")

            return NlpResult("Imposto volume a " + str(volume) + ".", action="set_volume", params={"volume" : volume})
        
        case "volume_up":
            return NlpResult("Ricevuto, eseguo", action="volume_up", params=None)
        case "volume_down":
            return NlpResult("Ricevuto, eseguo", action="volume_down", params=None)
        case "mute":
            return NlpResult("Ricevuto, eseguo", action="mute", params=None)     
        case "shelly":
            return NlpResult("STATUS CAMERA: ", action="luce", params="ON")       
        case _:
            return NlpResult("Non ho capito, puoi ripetere per favore?")
            
            
    """if "buon giorno" in user_text:
        return NlpResult("buongiorno a te!")
    elif "arrivederci" in user_text:
        return NlpResult("arrivederci!")
    elif "sveglia alle 7" in user_text:
        return NlpResult("Ok, in futuro qui imposterò davvero una sveglia alle 7.", "set_alarm", {"time" : "07:00"})
    else:
        return NlpResult("Non ho capito, puoi ripetere per favore?")"""


if __name__ == "__main__":
    get_response("imposto il volume zero")