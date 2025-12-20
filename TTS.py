from pathlib import Path
import subprocess
import json
import sounddevice as sd
from scipy.io import wavfile
import time
import queue

CFG = None


def load_tts_config() -> dict:
    """Load and return TTS configuration from JSON file."""
    
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / "tts_config.json"
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def text_to_wav(text : str, out_path : str | Path = "Traccia/tts_output.wav") -> Path:
    """Generates a WAV file from text using Piper."""
    
    global CFG
    
    if CFG == None:
        CFG = load_tts_config()
        
    piper_bin  = CFG["PIPER_BIN"]
    model_path 	 = CFG["MODEL_PATH"]
    default_lang = CFG["DEFAULT_LANGUAGE"]
    extra_args   = CFG.get("extra_args", [])
    
    out_path= Path(out_path)
    out_path.parent.mkdir(parents = True, exist_ok = True)
    
    cmd = [
        piper_bin,
        "--model", model_path,
        "--output_file", str(out_path)
    ] + extra_args
    
    result = subprocess.run(
        cmd,
        input = text,
        text = True,
        capture_output = True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"piper failed with code {result.returncode}:\n{result.stderr}")
    
    if not out_path.is_file():
        raise RuntimeError(f"TTS output file not found: {out_path}")
    
    return Path(out_path)

def speak(text : str):
    
    if not text:
        return
    
    start = time.perf_counter()
    print("0.00 - Start elaboration")
    
    wav_path = text_to_wav(text)
    
    sample_rate, data = wavfile.read(wav_path)  
    
    print(f"{(time.perf_counter() - start):.2f} - End elaboration")
      
    sd.play(data, samplerate = sample_rate)
    sd.wait()
    
    print(f"{(time.perf_counter() - start):.2f} - End reproduction")
    
    
if __name__ == "__main__":
    while True:
        s = input("Text to read: ").strip()
        if not s:
            break
        speak(s)
    