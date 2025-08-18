import os
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from .schemas import PatientData
from .ml_model import MLModel


# -------------------------
# Paths
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "diabetes_model.joblib"
METRICS_PATH = BASE_DIR / "model" / "metrics.json"

# -------------------------
# Initialize MLModel
# -------------------------
ml_model = MLModel(MODEL_PATH, METRICS_PATH)


# -------------------------
# Lifespan (startup/shutdown)
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await asyncio.to_thread(ml_model.load)
    except FileNotFoundError as e:
        print(f"⚠️ {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error loading model: {e}")
    yield


# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(
    title="Diabetes Prediction API",
    version="1.0.0",
    description="API for predicting diabetes using Pima Indians dataset",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

# -------------------------
# FastAPI CROS middleware
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # tighten this in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Health check
# -------------------------
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is operational"}


# -------------------------
# Model info
# -------------------------
@app.get("/info")
async def model_info():
    if ml_model.model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        feature_info = await asyncio.to_thread(ml_model.get_feature_info)
        return {
            "model_type": type(ml_model.model).__name__,
            "dataset": "Diabetes Dataset",
            "features": feature_info,
            "metrics": ml_model.get_metrics() or {},
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving model information: {str(e)}"
        )


# -------------------------
# Metrics
# -------------------------
@app.get("/metrics")
async def metrics():
    if ml_model.metrics is None:
        raise HTTPException(status_code=500, detail="Metrics not available")
    return ml_model.get_metrics()


# -------------------------
# Predict
# -------------------------
@app.post("/predict")
async def predict(request: PatientData):
    if ml_model.model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


# Serve static frontend files
BASE_DIR = os.path.dirname(__file__)
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True), name="static")