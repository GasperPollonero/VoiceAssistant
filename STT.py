import json
import subprocess
import time
import sounddevice as sd
from scipy.io import wavfile
from pathlib import Path

def load_stt_config() -> dict:
    """Load and return STT configuration from JSON file."""
    
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / "stt_config.json"
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)
    

def get_text_from_audiofile(path : str, lang : str | None = None, proc_time : bool = False) -> str:
    """Return the transcription of a WAV file.

    Args:
        path (str): Path to the wav file.
        lang (str | None, optional): Language to use for transcription. If None, the "DEFAULT_LANGUAGE" from stt_config.json is used.
        proc_time (bool, optional): If True, print the total transcription time. Defaults to False.

    Raises:
        FileNotFoundError: _description_
        RuntimeError: _description_
        RuntimeError: _description_

    Returns:
        str: the transcription of the audio file.
    """
    if proc_time:
        start = time.perf_counter()
        
        
    cfg = load_stt_config()
    whisper_bin  = cfg["WHISPER_BIN"]
    model_path 	 = cfg["MODEL_PATH"]
    default_lang = cfg["DEFAULT_LANGUAGE"]
    extra_args   = cfg.get("extra_args", [])
    
    audio_path = Path(path)
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    lang_to_use = lang or default_lang
    
    cmd = [
        whisper_bin,
        "-m", model_path,
        "-f", str(audio_path),
        "-l", lang_to_use,
    ] + extra_args
    
    # Runs the program and creates a audio_path.txt files with result
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"whisper-cli failed with code {result.returncode}:\n{result.stderr}")
        
    txt_path = audio_path.with_suffix(audio_path.suffix + ".txt")
    if not txt_path.is_file():
        raise RuntimeError(f"Output txt file not found: {txt_path}")
    
    with txt_path.open("r", encoding="utf-8") as f:
        text = f.read().strip()
    
    if proc_time:
        elapsed = time.perf_counter() - start
        print(f"[STT] {path} trascritto in: {elapsed:.2f} s")
        
    return text
    

def get_text_from_mic(max_seconds : int = 10) -> str:
    
    cfg = load_stt_config()
    fs  = cfg["SAMPLING_FREQUENCY"]
    channels = cfg["SAMPLING_CHANNELS"]
    
    #sd.default.samplerate = fs
    #sd.default.channels = channels
    #d.default.device = 1
    
    print("Parla ora... ")
    myrec = sd.rec(
        int(max_seconds * fs), 
        samplerate=fs, 
        channels=channels
        )
    
    sd.wait()
    
    print("...recording ended.")
    wavfile.write(data = myrec, rate = fs, filename="Traccia/temp_recording.wav")
    
    return get_text_from_audiofile("Traccia/temp_recording.wav")

if __name__ == "__main__":
    start = time.perf_counter()
    
    
    print(get_text_from_mic(5))
    
    
    #print(get_text_from_audiofile("Traccia/mentana.wav", proc_time=True))
    
    
    end = time.perf_counter()
    elapsed = end - start
    print(f"Tempo di esecuzione: {elapsed:.2f} s")
