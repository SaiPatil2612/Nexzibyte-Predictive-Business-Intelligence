
from pathlib import Path

import pandas as pd
import joblib

from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "synthetic"
    / "Day7_Synthetic_Quote_Modeling_Dataset.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "notebooks"
    / "models"
    / "Day7_Quote_Logistic_Model.joblib"
)

FEATURES = [
    "Quote_Value",
    "Discount_Pct",
    "Revision_Count",
    "Engagement_Count",
]

TARGET = "Won_Flag"

# Load existing synthetic modeling dataset
data = pd.read_csv(DATA_PATH)

X = data[FEATURES]
y = data[TARGET].astype(int)

# Reproduce the original Day 7 stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# Load the existing trained Logistic Regression pipeline
logistic_model = joblib.load(MODEL_PATH)

# Create a majority-class baseline
dummy_model = DummyClassifier(strategy="most_frequent")
dummy_model.fit(X_train, y_train)

# Generate predictions on the same test records
models = {
    "Logistic Regression": logistic_model,
    "Majority Class Baseline": dummy_model,
}

results = []

for model_name, model in models.items():
    predictions = model.predict(X_test)

    row = {
        "Model": model_name,
        "Test_Records": len(y_test),
        "Accuracy": accuracy_score(y_test, predictions),
        "Won_Precision": precision_score(
            y_test, predictions, zero_division=0
        ),
        "Won_Recall": recall_score(
            y_test, predictions, zero_division=0
        ),
        "Won_F1": f1_score(
            y_test, predictions, zero_division=0
        ),
    }

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_test)[:, 1]
        row["ROC_AUC"] = roc_auc_score(y_test, probabilities)
    else:
        row["ROC_AUC"] = None

    results.append(row)

comparison = pd.DataFrame(results)

print("\nDAY 7 QUOTATION MODEL VS BASELINE")
print("=" * 65)
print(comparison.to_string(index=False))

print("\nTest target distribution:")
print(y_test.value_counts().sort_index())

print("\nLogistic Regression classification report:")
print(
    classification_report(
        y_test,
        logistic_model.predict(X_test),
        target_names=["Lost", "Won"],
        zero_division=0,
    )
)

# Save a separate comparison report
output_path = (
    BASE_DIR
    / "reports"
    / "Day15_Quote_Model_vs_Baseline.csv"
)

comparison.to_csv(output_path, index=False)

print(f"\nComparison saved to: {output_path}")
print("\nOriginal dataset and trained model were not modified.")
