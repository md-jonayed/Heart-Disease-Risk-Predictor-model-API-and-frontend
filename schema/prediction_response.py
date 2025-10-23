from pydantic import BaseModel, Field
from typing import Dict, Optional


class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ..., description="Predicted category: 'Positive' or 'Negative'", example="Positive")
    confidence: Optional[float] = Field(
        None, description="Model's confidence score for the predicted class (0.0 - 1.0). None if unavailable.")
    class_probabilities: Optional[Dict[str, float]] = Field(
        None, description="Probability distribution across classes as {'0': prob0, '1': prob1}. None if unavailable.")
