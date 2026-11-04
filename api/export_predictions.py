
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "notebooks"
    / "models"
    / "Day7_Quote_Logistic_Model.joblib"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "Day14_API_Sample_Predictions.csv"
)

FEATURES = [
    "Quote_Value",
    "Discount_Pct",
    "Revision_Count",
    "Engagement_Count",
]

# Synthetic demonstration scenarios only
sample_data = pd.DataFrame([
    {
        "Quote_Value": 125000,
        "Discount_Pct": 10,
        "Revision_Count": 2,
        "Engagement_Count": 5,
    },
    {
        "Quote_Value": 1,
        "Discount_Pct": 100,
        "Revision_Count": 0,
        "Engagement_Count": 0,
    },
    {
        "Quote_Value": 85000,
        "Discount_Pct": 5,
        "Revision_Count": 1,
        "Engagement_Count": 8,
    },
    {
        "Quote_Value": 250000,
        "Discount_Pct": 15,
        "Revision_Count": 3,
        "Engagement_Count": 4,
    },
    {
        "Quote_Value": 50000,
        "Discount_Pct": 0,
        "Revision_Count": 0,
        "Engagement_Count": 2,
    },
], columns=FEATURES)

model = joblib.load(MODEL_PATH)

probabilities = model.predict_proba(sample_data)
predictions = model.predict(sample_data)

export_data = sample_data.copy()

export_data["Model_ID"] = "DAY7_QUOTE_LOGISTIC"
export_data["Predicted_Outcome"] = [
    "Won" if int(value) == 1 else "Lost"
    for value in predictions
]
export_data["Win_Probability"] = probabilities[:, 1]
export_data["Lost_Probability"] = probabilities[:, 0]
export_data["Data_Status"] = "Synthetic demonstration only"
export_data["Approval_Status"] = "Not approved for production use"

export_data.to_csv(OUTPUT_PATH, index=False)

print("Day 14 prediction export completed.")
print("Output:", OUTPUT_PATH)
print("Records exported:", len(export_data))
print("Probability totals:")
print(
    (
        export_data["Win_Probability"]
        + export_data["Lost_Probability"]
    ).round(6).tolist()
)
