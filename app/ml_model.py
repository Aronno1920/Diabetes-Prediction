import joblib
import numpy as np
import json
from pathlib import Path

class MLModel:
    """Wrapper for the diabetes ML model"""

    def __init__(self, model_path: Path, metrics_path: Path):
        self.model_path = model_path
        self.metrics_path = metrics_path
        self.model = None
        self.metrics = None

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError("Model file not found")
        self.model = joblib.load(self.model_path)
        if self.metrics_path.exists():
            with open(self.metrics_path, "r") as f:
                self.metrics = json.load(f)

    def predict(self, data: list):
        if self.model is None:
            raise ValueError("Model not loaded")
        X = np.array(data).reshape(1, -1)
        pred_class = int(self.model.predict(X)[0])
        confidence = float(self.model.predict_proba(X)[0][pred_class])
        return pred_class, confidence

    def get_metrics(self):
        return self.metrics
