# Import Required Library
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from pathlib import Path

from .schemas import PatientData
from .ml_model import MLModel
#############################

# Paths
MODEL_PATH = Path("../model/diabetes_model.joblib")
METRICS_PATH = Path("../model/metrics.json")

# Initialize MLModel
ml_model = MLModel(MODEL_PATH, METRICS_PATH)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(ml_model.load)
    yield

app = FastAPI(
    title="Diabetes Prediction API",
    version="1.0.0",
    description="API for predicting diabetes using Pima Indians dataset",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is operational"}

@app.get("/metrics")
async def metrics():
    if ml_model.metrics is None:
        raise HTTPException(status_code=500, detail="Metrics not available")
    return ml_model.get_metrics()

@app.post("/predict")
async def predict(request: PatientData):
    try:
        features = [
            request.Pregnancies,
            request.Glucose,
            request.BloodPressure,
            request.SkinThickness,
            request.Insulin,
            request.BMI,
            request.DiabetesPedigreeFunction,
            request.Age,
        ]
        pred_class, confidence = await asyncio.to_thread(
            ml_model.predict, features
        )
        result_text = "Diabetic" if pred_class == 1 else "Not Diabetic"
        return {
            "prediction": pred_class,
            "result": result_text,
            "confidence": confidence,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Prediction error")
