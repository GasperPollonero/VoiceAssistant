import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import sounddevice as sd
from queue import Queue, Full
import time

start = time.perf_counter()

# gives log info on vosk startup and model loading.
SetLogLevel(0)

# rate of audio sampling. Vosk takes only data at 16 kHz of sampling rate.
SAMPLERATE = 16000

# the size of each chunk of data put in the queue. 
# It corresponds to BLOCKSIZE/SAMPLERATE = seconds for each chunk.
BLOCKSIZE = 1000

# loads the model and initialize the Recognizer.
model = Model("./models/vosk/vosk-model-it-0.22")
rec = KaldiRecognizer(model, SAMPLERATE)

# removes all "debug" infos from output (i.e. timestamps, etc...).
rec.SetWords(False)
rec.SetPartialWords(False)

# data queue for audio chunks, multithreading-safe.
q_data : Queue[bytes] = Queue(maxsize=20)

# callback function of the InputStream thread.
def _callback(indata,frames,time,status):
    
    if status:
        pass
    
    # converts data into bytes for Vosk.
    data = indata.tobytes()
    
    try:
        q_data.put_nowait(data)
        
    except Full:
        print("CODA PIENA")

# starts sounddevice.InputStream thread.
# Vosk expects audio PCM 16-bit mono.
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
        
        # get the data from queue.
        data = q_data.get()
        
        # AcceptWaveform reutrns True if the word / sentence is "closed".
        if rec.AcceptWaveform(data):
            
            # get(key, default) gets value corresponding to key from a dictionary.
            # if key does not exists, returns default.
            text = json.loads(rec.Result()).get("text", "")
            if text:
                print("FINAL: ", text)
        else:
            
            partial = json.loads(rec.PartialResult()).get("partial", "")
            if partial:
                print("PARTIAL: ", partial)