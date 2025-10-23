import pandas as pd
import joblib
from typing import Any, Dict, Optional

try:
    with open("Model/xgb_heart_disease_prediction_model.joblib", "rb") as f:
        model = joblib.load(f)
except FileNotFoundError:
    print("Warning: Model file not found. Prediction endpoint will fail.")
    model = None

MODEL_VERSION = "V1"


def predict_output(user_input: Any) -> Dict[str, Optional[object]]:
    if hasattr(user_input, "dict"):
        input_dict = user_input.dict()
    elif isinstance(user_input, dict):
        input_dict = user_input
    else:
        try:
            input_dict = dict(user_input)
        except Exception:
            raise ValueError("Unsupported input type for prediction")

    input_df = pd.DataFrame([input_dict])

    if model is None:
        raise RuntimeError("ML model not loaded")

    predicted_category = None
    confidence = None
    class_probabilities = None

    try:
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_df)
            prob0 = float(proba[0][0])
            prob1 = float(proba[0][1])
            # predicted label based on threshold 0.5
            predicted_label = 1 if prob1 >= 0.5 else 0
            predicted_category = "Positive" if predicted_label == 1 else "Negative"
            confidence = round(max(prob0, prob1), 3)
            class_probabilities = {"0": prob0, "1": prob1}
        else:
            # fallback to predict() when predict_proba not available
            pred = model.predict(input_df)
            predicted_label = int(pred[0])
            predicted_category = "Positive" if predicted_label == 1 else "Negative"
            confidence = None
            class_probabilities = None
    except Exception as e:
        raise RuntimeError(f"Model prediction failed: {e}")

    return {
        "predicted_category": predicted_category,
        "confidence": confidence,
        "class_probabilities": class_probabilities
    }
