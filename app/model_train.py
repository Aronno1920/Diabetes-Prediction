import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Ensure model directory exists
os.makedirs("../model", exist_ok=True)

# 1. Load dataset
df = pd.read_csv("../sample_data/diabetes.csv")

# 2. Separate features & target
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# 3. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Define candidate models
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "RandomForest": RandomForestClassifier(),
    "SVM": SVC(probability=True),   # allow predict_proba
    "DecisionTree": DecisionTreeClassifier(),
    "KNN": KNeighborsClassifier()
}

best_model = None
best_score = 0
best_model_name = None
metrics_summary = {}

# 5. Train & evaluate models
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred)
    }
    metrics_summary[name] = metrics

    # Select best model based on F1-score
    if metrics["f1_score"] > best_score:
        best_model = model
        best_model_name = name
        best_score = metrics["f1_score"]

# 6. Save best model & metrics
model_path = "../model/diabetes_model.joblib"
joblib.dump(best_model, model_path)


metric_path = "../model/metrics.json"
with open(metric_path, "w") as f:
    json.dump({"best_model": best_model_name, "metrics": metrics_summary}, f, indent=4)

print(f"✅ Best model: {best_model_name}")
print(f"✅ Model saved to {model_path}")
print(f"✅ Metrics saved to {metric_path}")
