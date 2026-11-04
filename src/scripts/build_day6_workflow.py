from pathlib import Path
import nbformat

ROOT = Path.cwd()

NOTEBOOK = ROOT / "notebooks" / "04_lead_model_Day6_Enhanced_v2.ipynb"
BACKUP = ROOT / "notebooks" / "04_lead_model_Day6_Enhanced_v2_PreExtension.ipynb"
DATASET = ROOT / "data" / "processed" / "Day5_Feature_Dataset_v2.csv"

OUTPUTS = [
    ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Model_Comparison.csv",
    ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Calibration_Assessment.csv",
    ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Threshold_Analysis.csv",
    ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Scored_Output.csv",
    ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Priority_Queue.csv",
    ROOT / "models" / "Day6_Enhanced_v2_Demo_Model.joblib",
    ROOT / "reports" / "Day6_Enhanced_v2_Lead_Model_Evaluation.md",
]

if not NOTEBOOK.exists():
    raise FileNotFoundError(f"Notebook not found: {NOTEBOOK}")

if not BACKUP.exists():
    raise FileNotFoundError(f"Verified backup not found: {BACKUP}")

if not DATASET.exists():
    raise FileNotFoundError(f"Day 5 dataset not found: {DATASET}")

notebook = nbformat.read(NOTEBOOK, as_version=4)
backup = nbformat.read(BACKUP, as_version=4)

nbformat.validate(notebook)
nbformat.validate(backup)

if len(notebook.cells) != 2 or notebook.cells != backup.cells:
    raise RuntimeError(
        "Notebook no longer matches the verified backup. "
        "Stop for review; no files were changed."
    )

if any(path.exists() for path in OUTPUTS):
    existing = [str(path) for path in OUTPUTS if path.exists()]
    raise FileExistsError(
        "Refusing to overwrite existing outputs: " + ", ".join(existing)
    )

workflow = r'''
# Day 6 Enhanced Lead Model — Synthetic Demonstration
# IMPORTANT: The target labels below are randomly generated.
# Results are for technical demonstration only, NOT business performance.

from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, precision_score,
    recall_score, f1_score, roc_auc_score, average_precision_score,
    brier_score_loss, log_loss, confusion_matrix
)

ROOT = Path.cwd()
DATA_PATH = ROOT / "data" / "processed" / "Day5_Feature_Dataset_v2.csv"

OUTPUT_PATHS = {
    "comparison": ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Model_Comparison.csv",
    "calibration": ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Calibration_Assessment.csv",
    "thresholds": ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Threshold_Analysis.csv",
    "scored": ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Scored_Output.csv",
    "queue": ROOT / "data" / "synthetic" / "Day6_Enhanced_v2_Priority_Queue.csv",
    "model": ROOT / "models" / "Day6_Enhanced_v2_Demo_Model.joblib",
    "report": ROOT / "reports" / "Day6_Enhanced_v2_Lead_Model_Evaluation.md",
}

# Refuse to overwrite any existing Day 6 deliverables.
existing = [str(path) for path in OUTPUT_PATHS.values() if path.exists()]
if existing:
    raise FileExistsError("No outputs were written. Existing files: " + ", ".join(existing))

df = pd.read_csv(DATA_PATH)

CATEGORICAL_FEATURES = [
    "Industry / Sub-industry",
    "Target Customers / B2B or B2C",
]
NUMERIC_FEATURES = [
    "Founded Year (Standardized)",
    "Employee Count (Numeric)",
    "Company Age (Years)",
]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES

missing = [col for col in FEATURES if col not in df.columns]
if missing:
    raise ValueError(f"Missing required features: {missing}")

if "Company Name" not in df.columns:
    raise ValueError("Company Name column is required for output identification.")

# Create a reproducible RANDOM target strictly for technical testing.
# This is not a verified conversion outcome and must not be used for business decisions.
rng = np.random.default_rng(42)
synthetic_target = rng.binomial(1, 0.35, size=len(df))

if len(np.unique(synthetic_target)) != 2:
    raise ValueError("Synthetic target contains only one class; stop for review.")

X = df[FEATURES].copy()
y = pd.Series(synthetic_target, index=df.index, name="Synthetic_Demo_Target")

train_idx, test_idx = train_test_split(
    df.index.to_numpy(),
    test_size=0.25,
    random_state=42,
    stratify=y
)

X_train = X.loc[train_idx]
X_test = X.loc[test_idx]
y_train = y.loc[train_idx]
y_test = y.loc[test_idx]

def make_preprocessor():
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer([
        ("numeric", numeric_pipeline, NUMERIC_FEATURES),
        ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
    ])

model_specs = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Logistic Regression Balanced": LogisticRegression(
        max_iter=1000, class_weight="balanced", random_state=42
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200, random_state=42, min_samples_leaf=2
    ),
    "Random Forest Balanced": RandomForestClassifier(
        n_estimators=200, random_state=42, min_samples_leaf=2,
        class_weight="balanced"
    ),
    "Hist Gradient Boosting": HistGradientBoostingClassifier(
        max_iter=100, random_state=42
    ),
    "Hist Gradient Boosting Balanced": HistGradientBoostingClassifier(
        max_iter=100, random_state=42, class_weight="balanced"
    ),
}

def calculate_metrics(name, actual, probabilities):
    predictions = (probabilities >= 0.5).astype(int)
    return {
        "Model": name,
        "Accuracy": accuracy_score(actual, predictions),
        "Balanced Accuracy": balanced_accuracy_score(actual, predictions),
        "Precision": precision_score(actual, predictions, zero_division=0),
        "Recall": recall_score(actual, predictions, zero_division=0),
        "F1": f1_score(actual, predictions, zero_division=0),
        "ROC_AUC": roc_auc_score(actual, probabilities),
        "Average_Precision": average_precision_score(actual, probabilities),
    }

fitted_models = {}
comparison_rows = []

for name, estimator in model_specs.items():
    pipeline = Pipeline([
        ("preprocessor", make_preprocessor()),
        ("model", estimator),
    ])
    pipeline.fit(X_train, y_train)
    probabilities = pipeline.predict_proba(X_test)[:, 1]
    comparison_rows.append(calculate_metrics(name, y_test, probabilities))
    fitted_models[name] = pipeline

comparison = pd.DataFrame(comparison_rows).sort_values(
    "ROC_AUC", ascending=False
).reset_index(drop=True)

# Calibrate a balanced logistic regression pipeline using training data only.
base_pipeline = Pipeline([
    ("preprocessor", make_preprocessor()),
    ("model", LogisticRegression(
        max_iter=1000, class_weight="balanced", random_state=42
    )),
])

calibrated_model = CalibratedClassifierCV(
    estimator=base_pipeline,
    method="sigmoid",
    cv=3
)
calibrated_model.fit(X_train, y_train)

raw_model = fitted_models["Logistic Regression Balanced"]
raw_probabilities = raw_model.predict_proba(X_test)[:, 1]
calibrated_probabilities = calibrated_model.predict_proba(X_test)[:, 1]

calibration_rows = []
for name, probabilities in [
    ("Balanced Logistic Regression - Uncalibrated", raw_probabilities),
    ("Balanced Logistic Regression - Sigmoid Calibrated", calibrated_probabilities),
]:
    calibration_rows.append({
        "Model": name,
        "Brier Score": brier_score_loss(y_test, probabilities),
        "Log Loss": log_loss(y_test, probabilities, labels=[0, 1]),
        "ROC_AUC": roc_auc_score(y_test, probabilities),
        "Average_Precision": average_precision_score(y_test, probabilities),
        "Evaluation": "Synthetic demonstration only",
    })

calibration = pd.DataFrame(calibration_rows)

threshold_rows = []
for threshold in [0.30, 0.40, 0.50, 0.60, 0.70]:
    predictions = (calibrated_probabilities >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(
        y_test, predictions, labels=[0, 1]
    ).ravel()

    threshold_rows.append({
        "Threshold": threshold,
        "Precision": precision_score(y_test, predictions, zero_division=0),
        "Recall": recall_score(y_test, predictions, zero_division=0),
        "F1": f1_score(y_test, predictions, zero_division=0),
        "True Positives": int(tp),
        "False Positives": int(fp),
        "True Negatives": int(tn),
        "False Negatives": int(fn),
        "Predicted Positive Count": int(predictions.sum()),
        "Status": "Exploratory only; no approved business threshold",
    })

threshold_analysis = pd.DataFrame(threshold_rows)

# Score the held-out test rows only. These probabilities are not real lead-conversion
# probabilities because the target was generated randomly.
scored = df.loc[test_idx, ["Company Name"] + FEATURES].copy()
scored.insert(0, "Source_Row_Index", test_idx)
scored["Synthetic_Demo_Target"] = y_test.to_numpy()
scored["Demo_Probability"] = calibrated_probabilities
scored["Demo_Prediction_At_0_50"] = (calibrated_probabilities >= 0.50).astype(int)
scored["Data_Status"] = "SYNTHETIC DEMONSTRATION ONLY"

priority_queue = scored.sort_values(
    "Demo_Probability", ascending=False
).reset_index(drop=True)
priority_queue.insert(0, "Demo_Rank", np.arange(1, len(priority_queue) + 1))
priority_queue["Demo_Priority_Band"] = np.where(
    priority_queue["Demo_Rank"] <= 10, "High (demo)",
    np.where(priority_queue["Demo_Rank"] <= 25, "Medium (demo)", "Low (demo)")
)
priority_queue["Business_Approval_Status"] = "NOT APPROVED FOR BUSINESS USE"

def markdown_table(frame):
    columns = [str(col) for col in frame.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in frame.iterrows():
        values = []
        for value in row:
            if isinstance(value, (float, np.floating)):
                value = f"{value:.4f}"
            text = str(value).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)

# Final overwrite guard immediately before saving.
existing = [str(path) for path in OUTPUT_PATHS.values() if path.exists()]
if existing:
    raise FileExistsError("No outputs were written. Existing files: " + ", ".join(existing))

comparison.to_csv(OUTPUT_PATHS["comparison"], index=False)
calibration.to_csv(OUTPUT_PATHS["calibration"], index=False)
threshold_analysis.to_csv(OUTPUT_PATHS["thresholds"], index=False)
scored.to_csv(OUTPUT_PATHS["scored"], index=False)
priority_queue.to_csv(OUTPUT_PATHS["queue"], index=False)

joblib.dump({
    "model": calibrated_model,
    "features": FEATURES,
    "categorical_features": CATEGORICAL_FEATURES,
    "numeric_features": NUMERIC_FEATURES,
    "synthetic_target": True,
    "random_seed": 42,
    "test_threshold": 0.50,
    "warning": "Demonstration model only. Not validated for business use.",
}, OUTPUT_PATHS["model"])

report = f"""# Day 6 — Lead Model Evaluation

## Status
**Technical demonstration completed; business validation remains pending.**

## Important limitation
The dataset does not contain verified lead-conversion outcomes. A reproducible random target was generated for testing the modeling workflow. All scores, probabilities, rankings, calibration results, and threshold results are synthetic demonstration outputs. They must not be interpreted as real NexziByte performance or used to make production decisions.

## Dataset and split
- Input dataset: `data/processed/Day5_Feature_Dataset_v2.csv`
- Dataset rows: {len(df)}
- Training rows: {len(train_idx)}
- Test rows: {len(test_idx)}
- Synthetic positive labels: {int(y.sum())}
- Synthetic negative labels: {int((1-y).sum())}
- Random seed: 42
- Train/test split: 75% / 25%, stratified

## Model features
{", ".join(FEATURES)}

Company names, pre-existing score fields, and data-quality flags were excluded from model inputs.

## Model comparison
All metrics use the held-out synthetic test set and a 0.50 demonstration threshold.

{markdown_table(comparison)}

## Calibration assessment
Brier score and log loss are included as diagnostic measures. Calibration on random synthetic labels does not establish useful real-world probability estimates.

{markdown_table(calibration)}

## Threshold analysis
No business threshold has been approved. Thresholds are shown for technical exploration only.

{markdown_table(threshold_analysis)}

## Generated artifacts
- `data/synthetic/Day6_Enhanced_v2_Model_Comparison.csv`
- `data/synthetic/Day6_Enhanced_v2_Calibration_Assessment.csv`
- `data/synthetic/Day6_Enhanced_v2_Threshold_Analysis.csv`
- `data/synthetic/Day6_Enhanced_v2_Scored_Output.csv`
- `data/synthetic/Day6_Enhanced_v2_Priority_Queue.csv`
- `models/Day6_Enhanced_v2_Demo_Model.joblib`

## Business validation required before production
1. Obtain verified historical lead outcomes and define the prediction horizon.
2. Confirm the target definition with the business owner.
3. Validate the dataset for temporal leakage and representativeness.
4. Establish the cost of false positives, false negatives, and sales follow-up capacity.
5. Select a threshold based on agreed business costs and capacity.
6. Evaluate on a time-based holdout and compare with a baseline.
7. Obtain business approval before operational use.

## Day 6 conclusion
The workflow demonstrates model comparison, class-weighted alternatives, probability calibration assessment, threshold analysis, and ranked demonstration output. It does **not** establish predictive business value because the target is synthetic. Business validation and threshold approval remain pending.
"""

OUTPUT_PATHS["report"].write_text(report, encoding="utf-8")

print("Day 6 modeling workflow completed.")
print(f"Rows: {len(df)} | Training: {len(train_idx)} | Test: {len(test_idx)}")
print("All outputs are synthetic demonstration artifacts.")
print("\nModel comparison:")
display(comparison)
print("\nCalibration assessment:")
display(calibration)
print("\nThreshold analysis:")
display(threshold_analysis)
print("\nPriority queue preview:")
display(priority_queue.head(10))
print("\nCreated artifacts:")
for name, path in OUTPUT_PATHS.items():
    print(f"{name}: {path.relative_to(ROOT)}")
'''

notebook.cells.append(
    nbformat.v4.new_markdown_cell(
        "## Day 6 enhanced modeling workflow\n\n"
        "The following cell compares models, assesses class weighting and calibration, "
        "explores thresholds, and creates a demonstration scoring queue. "
        "**The target is randomly generated; results are not real business performance.**"
    )
)
notebook.cells.append(nbformat.v4.new_code_cell(workflow))

nbformat.validate(notebook)

temporary_path = NOTEBOOK.with_suffix(".tmp.ipynb")
nbformat.write(notebook, temporary_path)

# Validate the temporary notebook before replacing the target notebook.
check = nbformat.read(temporary_path, as_version=4)
nbformat.validate(check)

if len(check.cells) != 4:
    temporary_path.unlink(missing_ok=True)
    raise RuntimeError("Unexpected notebook cell count. Original notebook was not replaced.")

temporary_path.replace(NOTEBOOK)

print("Day 6 notebook updated successfully.")
print(f"Notebook cells: {len(check.cells)}")
print("Original two cells preserved; two workflow cells appended.")
print("Verified pre-extension backup preserved.")
print("No model outputs have been generated yet.")