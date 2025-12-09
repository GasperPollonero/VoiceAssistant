from pathlib import Path
import subprocess
import json
import sounddevice as sd
from scipy.io import wavfile

def load_tts_config() -> dict:
    """Load and return TTS configuration from JSON file."""
    
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / "tts_config.json"
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def text_to_wav(text : str, out_path : str | Path = "Traccia/tts_output.wav") -> Path:
    """Generates a WAV file from text using Piper."""
    
    cfg = load_tts_config()
    piper_bin  = cfg["PIPER_BIN"]
    model_path 	 = cfg["MODEL_PATH"]
    default_lang = cfg["DEFAULT_LANGUAGE"]
    extra_args   = cfg.get("extra_args", [])
    
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
    
    wav_path = text_to_wav(text)
    
    sample_rate, data = wavfile.read(wav_path)    
    sd.play(data, samplerate = sample_rate)
    sd.wait()
    
    
if __name__ == "__main__":
    while True:
        s = input("Text to read: ").strip()
        if not s:
            break
        speak(s)
    