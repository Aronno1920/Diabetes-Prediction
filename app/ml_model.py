import joblib
import numpy as np
import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict


class MLModel:
    """
    Wrapper for a scikit-learn ML model for Diabetes prediction.
    Handles model loading, prediction, metrics retrieval, and feature info.
    """

    def __init__(self, model_path: Path, metrics_path: Path):
        self.model_path: Path = model_path
        self.metrics_path: Path = metrics_path
        self.model = None
        self.metrics: Optional[Dict] = None

    def load(self) -> None:
        """
        Load the ML model and metrics from disk.
        Raises FileNotFoundError if model file is missing.
        """
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found at {self.model_path}")

        self.model = joblib.load(self.model_path)

        if self.metrics_path.exists():
            try:
                with open(self.metrics_path, "r", encoding="utf-8") as f:
                    self.metrics = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Metrics file at {self.metrics_path} is not valid JSON.")
                self.metrics = None

        print("✅ Model loaded successfully.")


    def predict(self, data: List[float]) -> Tuple[int, float]:
        """
        Predict the class (0 or 1) and confidence for the given input data.
        :param data: List of feature values
        :return: Tuple of predicted class and confidence
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call `.load()` first.")

        X = np.array(data).reshape(1, -1)
        pred_class = int(self.model.predict(X)[0])

        if hasattr(self.model, "predict_proba"):
            confidence = float(self.model.predict_proba(X)[0][pred_class])
        else:
            confidence = 1.0  # fallback if model doesn't support predict_proba

        return pred_class, confidence


    def get_metrics(self) -> Optional[Dict]:
        """
        Return the stored metrics of the model, if available.
        """
        return self.metrics


    def get_feature_info(self) -> List[str]:
        """
        Return the feature names of the model if available.
        Falls back to generic names if not present.
        """
        if self.model is None:
            return ["Model not loaded. Call `.load()` first."]

        if hasattr(self.model, "feature_names_in_"):
            return list(self.model.feature_names_in_)

        elif hasattr(self.model, "n_features_in_"):
            return [f"feature_{i}" for i in range(self.model.n_features_in_)]

        else:
            return ["feature_unknown"]
