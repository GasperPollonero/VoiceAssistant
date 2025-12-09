from pathlib import Path
import joblib
#from typing import Any

_VECTORIZER = None
_CLASSIFIER = None

    
def _load_intent_model(model_dir : str | Path = "models/intent") -> None:
    """ Loads vectorizer and classifier. """
    
    global _VECTORIZER, _CLASSIFIER
    
    if _VECTORIZER is not None and _CLASSIFIER is not None:
        return # already loaded
    
    model_dir = Path(model_dir)
    vec_path = model_dir / "intent_vectorizer.joblib"
    clf_path = model_dir / "intent_classifier.joblib"
    
    _VECTORIZER = joblib.load(vec_path)
    _CLASSIFIER = joblib.load(clf_path)

def predict_intent(input_text : str, threshold : float = 0.3) -> str:
    """Returns predicted intent or 'unknown' if confidence is too low. """
    
    _load_intent_model()
    
    X = _VECTORIZER.transform([input_text])
    
    probs = _CLASSIFIER.predict_proba(X)[0]
    
    max_proba = probs.max()
    best_index = probs.argmax()
    best_class = _CLASSIFIER.classes_[best_index]
    
    if max_proba < threshold:
        return "unknown", max_proba
    
    return best_class, max_proba

if __name__ == "__main__":
    while True:
        s = input("Text (leave empty for exit): ").strip()
        if not s:
            break
        intent, prob = predict_intent(s)
        print("Intent: " + intent + " prob: " + str(prob))