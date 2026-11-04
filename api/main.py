
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "notebooks" / "models" / "Day7_Quote_Logistic_Model.joblib"

# Load the verified quotation model
model = joblib.load(MODEL_PATH)

FEATURES = [
    "Quote_Value",
    "Discount_Pct",
    "Revision_Count",
    "Engagement_Count",
]

app = FastAPI(
    title="NexziByte Predictive BI API",
    description=(
        "Educational API prototype for synthetic quotation "
        "win classification. Not approved for production use."
    ),
    version="1.0.0",
)


class QuotePredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quote_value: float = Field(gt=0)
    discount_pct: float = Field(ge=0, le=100)
    revision_count: int = Field(ge=0)
    engagement_count: int = Field(ge=0)


class QuotePredictionResponse(BaseModel):
    model_id: str
    quote_value: float
    predicted_outcome: str
    win_probability: float
    lost_probability: float
    data_status: str
    approval_status: str


@app.get("/")
def root():
    return {
        "message": "NexziByte Predictive BI API is running",
        "model_id": "DAY7_QUOTE_LOGISTIC",
        "data_status": "Synthetic demonstration only",
        "production_approved": False,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
    }


@app.post(
    "/api/v1/predict/quotation",
    response_model=QuotePredictionResponse,
)
def predict_quotation(request: QuotePredictionRequest):
    input_data = pd.DataFrame(
        [
            {
                "Quote_Value": request.quote_value,
                "Discount_Pct": request.discount_pct,
                "Revision_Count": request.revision_count,
                "Engagement_Count": request.engagement_count,
            }
        ],
        columns=FEATURES,
    )

    probabilities = model.predict_proba(input_data)[0]
    predicted_class = int(model.predict(input_data)[0])

    win_probability = float(probabilities[1])
    lost_probability = float(probabilities[0])

    return {
        "model_id": "DAY7_QUOTE_LOGISTIC",
        "quote_value": request.quote_value,
        "predicted_outcome": (
            "Won" if predicted_class == 1 else "Lost"
        ),
        "win_probability": round(win_probability, 6),
        "lost_probability": round(lost_probability, 6),
        "data_status": "Synthetic demonstration only",
        "approval_status": "Not approved for production use",
    }
