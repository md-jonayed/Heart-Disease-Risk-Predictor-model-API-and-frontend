from pydantic import BaseModel, Field
from typing import Annotated, Literal


class PredictionInput(BaseModel):
    age: Annotated[int,
                   Field(..., description="Age of the patient in years", gt=0, lt=120)]
    sex: Annotated[Literal[0, 1],
                   Field(..., description="Sex (1 = male, 0 = female)")]
    cp: Annotated[Literal[0, 1, 2, 3], Field(
        ..., description="Chest pain type (0 = typical angina, 1 = atypical angina, 2 = non-anginal pain, 3 = asymptomatic)")]
    trestbps: Annotated[int,
                        Field(..., description="Resting blood pressure (mm Hg)", ge=50, le=250)]
    chol: Annotated[int,
                    Field(..., description="Serum cholesterol (mg/dl)", ge=100, le=700)]
    fbs: Annotated[Literal[0, 1],
                   Field(..., description="Fasting blood sugar > 120 mg/dL? (1 = True, 0 = False)")]
    restecg: Annotated[Literal[0, 1, 2], Field(
        ..., description="Resting ECG results (0 = normal, 1 = ST-T abnormality, 2 = left ventricular hypertrophy)")]
    thalach: Annotated[int,
                       Field(..., description="Maximum heart rate achieved", ge=40, le=250)]
    exang: Annotated[Literal[0, 1],
                     Field(..., description="Exercise-induced angina (1 = yes, 0 = no)")]
    oldpeak: Annotated[float, Field(
        ..., description="ST depression induced by exercise relative to rest", ge=0.0, le=10.0)]
    slope: Annotated[Literal[0, 1, 2], Field(
        ..., description="Slope of the peak exercise ST segment (0 = upsloping, 1 = flat, 2 = downsloping)")]
    ca: Annotated[Literal[0, 1, 2, 3],
                  Field(..., description="Number of major vessels (0–3) colored by fluoroscopy")]
    thal: Annotated[Literal[1, 2, 3], Field(
        ..., description="Thalassemia (1 = normal, 2 = fixed defect, 3 = reversible defect)")]
