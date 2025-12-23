import numpy as np
import joblib
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from wake_word_dataset import build_ww_dataset

def train_ww_model(model_dir : str | Path = "models/wakeword") -> None:
    X,y = build_ww_dataset()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    clf = LogisticRegression(
        max_iter = 1000,
        class_weight = "balanced"
    )
    clf.fit(X_train_scaled, y_train)
    
    train_acc = clf.score(X_train_scaled, y_train)
    test_acc = clf.score(X_test_scaled, y_test)
    print(f"Train accuracy: {train_acc:.3f}")
    print(f"Test accuracy: {test_acc:.3f}")
    
    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(scaler, model_dir / "ww_scaler.joblib")
    joblib.dump(clf, model_dir / "ww_classifier.joblib")
    

if __name__ == "__main__":
    train_ww_model()