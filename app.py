from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Imports from external modules
from schema.user_input import PredictionInput
from Model.predict import predict_output, model, MODEL_VERSION
from schema.prediction_response import PredictionResponse


# Initialize FastAPI App
app = FastAPI(
    title="Heart Disease Prediction API",
    description="Predict the presence of heart disease using patient data. "
                "Fields with fixed choices are shown as dropdowns in Swagger UI.",
    version="1.0"
)

# Enable CORS for local frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Prediction Endpoint
@app.post("/predict", response_model=PredictionResponse)
def predict_heart_disease(data: PredictionInput):
    if model is None:
        raise HTTPException(
            status_code=503, detail="Service Unavailable: ML Model failed to load.")

    try:
        result = predict_output(data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Prediction error: {str(e)}")


# Health Check Endpoint
@app.get("/health_check")
def health_check():
    """Checks the health of the application and model loading status."""
    if model is not None:
        return {
            "status": "ok",
            "model_loaded": True,
            "version": MODEL_VERSION
        }
    else:
        raise HTTPException(
            status_code=503, detail="Service Unavailable: ML Model not loaded.")


# Root Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Heart Disease Prediction API! Use /docs to test the endpoint."}


"""
{
    "age": 53,
    "sex": 1,
    "cp": 0,
    "trestbps": 140,
    "chol": 203,
    "fbs": 1,
    "restecg": 0,
    "thalach": 155,
    "exang": 1,
    "oldpeak": 3.1,
    "slope": 0,
    "ca": 0,
    "thal": 3
}
"""
