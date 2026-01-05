import json
import sounddevice as sd
from pathlib import Path
from vosk import KaldiRecognizer, Model, SetLogLevel
from queue import Queue, Full

class STT:
    
    def __init__(self):
        
        # configuration dictionary.
        self.cfg : dict
        # vosk class which transform speech to text.
        self.rec : KaldiRecognizer
        # data queue for audio chunks, multithreading-safe.
        self.q_data : Queue[bytes] = Queue(maxsize=20)


    def initialize_STT(self):
        """Loads vosk configuration and model."""
        self.cfg = self.load_stt_config()
        model = Model(self.cfg["MODEL_PATH"])
        self.rec = KaldiRecognizer(model, self.cfg["SAMPLING_FREQUENCY"])
    
    def load_stt_config(self) -> dict:
        """Load and return STT configuration from JSON file."""
        
        base_dir = Path(__file__).resolve().parent
        config_path = base_dir / "config" / "stt_config_vosk.json"
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
        
    # callback function of the InputStream thread.
    def _callback(self, indata, time, frames, status):
        
        # converts data into bytes for Vosk.
        data = indata.tobytes()
        
        try:
            self.q_data.put(data)
        except Full:
            print("STT queue is full!")
        
    def get_text_from_mic(self, max_seconds : int = -1) -> str:
        
        # clear queue.
        self.q_data = Queue()
        
        # starts listening.
        with sd.InputStream(
            samplerate=self.cfg["SAMPLING_FREQUENCY"],
            blocksize=self.cfg["BLOCKSIZE"],
            channels=1,
            callback=self._callback,
            dtype="int16"
        ):
            print("Parla ora... ")
            
            while True:
                data = self.q_data.get()
                # when sentence is completed stop listening.
                if self.rec.AcceptWaveform(data):
                    break
            
            # closes InputStream() and returns Vosk result.
            return json.loads(self.rec.Result()).get("text", "")

           
# main section for testing.
if __name__ == "__main__":
    
    stt = STT()
    stt.initialize_STT()
    
    while True:
        text = input("READY")
        if text == "a":
            print(stt.get_text_from_mic())
    
