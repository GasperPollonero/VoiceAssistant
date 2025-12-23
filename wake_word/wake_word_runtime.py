from pathlib import Path
import joblib

_SCALER = None
_CLASSIFIER = None

def _load_ww_model(model_dir : str | Path = "models/wakeword") -> None:
    
    global _SCALER, _CLASSIFIER
    
    if _SCALER is not None and _CLASSIFIER is not None:
        return
    
    model_dir = Path(model_dir)
    scal_path = model_dir / "ww_scaler.joblib"
    clf_path = model_dir / "ww_classifier.joblib"
    
    _SCALER = joblib.load(scal_path)
    _CLASSIFIER = joblib.load(clf_path)
    
def evaluate_audio(wav_path : str | Path = "prova.wav", threshold : float = 0.8):

    _load_ww_model()
    
    X = _SCALER.transform([])