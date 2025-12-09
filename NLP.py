from dataclasses import dataclass
from typing import Any, Sequence # Sequence is a generic type for every type that behaves like a list (es. list, tuple, etc.)
from intent_ml import predict_intent

@dataclass
class NlpResult:
    reply_text : str
    action : str | None = None
    params : dict[str, Any] | None = None
    
def get_response(user_text: str, user_id : str | None = None, history: Sequence[str] | None = None) -> NlpResult:
    
    user_text = user_text.lower()
    intent, prob = predict_intent(user_text)
    
    match intent:
        case "greeting":
            return NlpResult("buongiorno a te!")
        case "goodbye":
            return NlpResult("arrivederci!")
        case "volume_up":
            return NlpResult("Ricevuto, eseguo", action="volume_up", params=None)
        case "volume_down":
            return NlpResult("Ricevuto, eseguo", action="volume_down", params=None)
        case "mute":
            return NlpResult("Ricevuto, eseguo", action="mute", params=None)            
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
