import numpy as np
import json
import librosa
from pathlib import Path

def load_wav(path : str | Path = None):
    
    if path is str:
        path = Path(path)
        

def extract_mfcc_mean(wav_path : str | Path, sr : int = 16000, n_mfcc : int = 13) -> np.ndarray:
    
    if wav_path is str:
        wav_path = Path(path)
        
    y, sr = librosa.load(wav_path, sr=sr)  # carica audio e fa resampling a 16 kHz
    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc = n_mfcc,          # numero di coefficienti
        n_fft = 400,          # finestra ~25 ms a 16 kHz
        hop_length = 160,     # passo ~10 ms
    )
    # mfcc ha shape (n_mfcc, n_frames)

    # poi puoi fare la media nel tempo:
    return mfcc.mean(axis=1)   # shape: (n_mfcc,)
 
def build_ww_dataset(base_dir : str | Path = "D:\Cpp\Databases\WakeWord") -> tuple[np.ndarray, np.ndarray]:
    base = Path(base_dir)
    pos_dir = base / "Positives"
    neg_dir = base / "Negatives"
    
    X_list : list[np.darray] = []
    y_list : list[int] = []
    
    # label : 1 = wake word, 0 = background
    
    for wav_path in pos_dir.glob("*.wav"):
        feat = extract_mfcc_mean(wav_path)
        X_list.append(feat)
        y_list.append(1)
        
    for wav_path in neg_dir.glob("*.wav"):
        feat = extract_mfcc_mean(wav_path)
        X_list.append(feat)
        y_list.append(0)
        
    X = np.vstack(X_list)
    y = np.array(y_list)
    
    return X,y
   
if __name__ == "__main__":
    X, y = build_ww_dataset()
    print("X shape: ", X.shape)
    print("y shape: ", y.shape)
    print("Positives: ", (y == 1).sum(), "Negatives: ", (y == 0).sum())
    