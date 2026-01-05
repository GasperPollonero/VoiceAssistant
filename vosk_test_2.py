import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import sounddevice as sd
from queue import Queue, Full
import time

start = time.perf_counter()

SetLogLevel(0)

SAMPLERATE = 16000
BLOCKSIZE = 1000

model = Model("./models/vosk/vosk-model-it-0.22")
rec = KaldiRecognizer(model, SAMPLERATE)

rec.SetWords(False)
rec.SetPartialWords(False)

q_data : Queue[bytes] = Queue(maxsize=20)

def _callback(indata,frames,time,status):
    
    if status:
        pass
    
    data = indata.tobytes()
    
    try:
        q_data.put_nowait(data)
        
    except Full:
        print("CODA PIENA")
    
with sd.InputStream(
    samplerate=SAMPLERATE,
    blocksize=BLOCKSIZE,
    channels=1,
    callback=_callback,
    dtype="int16"
    ):
    end = time.perf_counter() - start
    print(f"Pronto in {end} s.\nParla pure...")
    while True:
        data = q_data.get()
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "")
            if text:
                print("FINAL: ", text)
        else:
            partial = json.loads(rec.PartialResult()).get("partial", "")
            if partial:
                print("PARTIAL: ", partial)