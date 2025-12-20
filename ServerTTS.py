import subprocess
import threading
import queue      # thread-safe list of FIFO type (First In First Out)
import json
from pathlib import Path

import numpy as np
import sounddevice as sd

def load_tts_config() -> dict:
    """Load and return TTS configuration from JSON file."""
    
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / "tts_config.json"
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)

class PiperTTS:
    
    def __init__(self, config_path : str | Path = ""):
        
        self.cfg = load_tts_config()
        self.proc = None
        self.audio_thread = None
        self.audio_queue = queue.Queue()
        
        self.sample_rate : int = self.cfg["SAMPLE_RATE"]
        self.channels : int = self.cfg["CHANNELS"]
        self.block_size : int = self.cfg["BLOCK_SIZE"]
        
        self._reader_thread : threading.Thread | None = None
        self._stop_flag : threading.Event = threading.Event()
        self._stream : sd.OutputStream | None = None
        
        
    def start(self):
        """ Runs Piper in persistent mode. """
        
        if self.proc is not None:
            return # already running
        
        args = [
            self.cfg["PIPER_BIN"], 
            "--model", self.cfg["MODEL_PATH"],
            "--output-raw",
            "--output-file", "-", # stdout
        ]
        extra = self.cfg.get("extra_args", [])
        args.extend(extra)
        
        self.proc = subprocess.Popen(
            args,
            stdin  = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.DEVNULL,
            bufsize= 0
        )
        
        self._stop_flag.clear()
        
        self._reader_thread = threading.Thread(
            target = self._audio_reader_loop,
            daemon = True
        )
        
        self._reader_thread.start()
        
        self._stream = sd.OutputStream(
            samplerate = self.sample_rate,
            channels = self.channels,
            dtype = "int16",
            blocksize = self.block_size,
            callback = self._audio_callback
        )
        
        self._stream.start()
    
    def stop(self):
        """ Stops stream audio and Piper. """
        
        self._stop_flag.set()
        
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
            
        if self.proc is not None:
             
            try:
                self.proc.stdin.close()
            except Exception:
                pass
            self.proc.terminate()
            self.proc = None
        
        
    def _audio_reader_loop(self):
        """ Reads from piper.stdout and fills the queue with audio bits. """
        assert self.proc is not None and self.proc.stdout is not None # same as if (condition) : raise AssesionError
        
        bytes_per_sample = 2 * self.channels # int16 = 2 byte
        chunk_bytes = self.block_size * bytes_per_sample
        
        while not self._stop_flag.is_set():
            raw = self.proc.stdout.read(chunk_bytes)
            if not raw:
                break # Piper closed stdout
            
            data = np.frombuffer(raw, dtype=np.int16) # converts byte into array
            
            if self.channels > 1:
                data = data.reshape(-1, self.channels)
                
                
            self.audio_queue.put(data) # bloks thread execution until the queue has enough space
            """try:
                self.audio_queue.put(data, timeout=0.5)
            except queue.Full:
                pass"""
            

    def _audio_callback(self, outdata, frames, time, status):
        
        """try:
            chunk = self.audio_queue.get_nowait()
        except queue.Empty:
            # No audio ready -> silence
            outdata[:] = 0
            return"""
        chunk = self.audio_queue.get()
        print("HERE")
        # if chunk is shorter fill till its length 
        if len(chunk) < frames:
            outdata[:len(chunk)] = chunk.reshape(-1, self.channels)
            outdata[len(chunk):] = 0
        else:
            outdata[:] = chunk[:frames].reshape(-1, self.channels)
        
    def speak(self, text : str):
        """ Sends text to Piper: it generates audio that will end to stream """
        
        if not text or self.proc is None or self.proc.stdin is None:
            return
        
        line = (text.strip() + "\n").encode("utf-8")
        self.proc.stdin.write(line)
        self.proc.stdin.flush()
        

if __name__ == "__main__":
    server = PiperTTS()
    server.start()
    server.speak("ciao come stai? Io sto bene.")
    while server.audio_queue.empty():
        print(server.audio_queue.qsize())
    server.stop()