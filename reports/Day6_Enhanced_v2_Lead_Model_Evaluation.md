# Day 6 — Lead Model Evaluation

## Status
**Technical demonstration completed; business validation remains pending.**

## Important limitation
The dataset does not contain verified lead-conversion outcomes. A reproducible random target was generated for testing the modeling workflow. All scores, probabilities, rankings, calibration results, and threshold results are synthetic demonstration outputs. They must not be interpreted as real NexziByte performance or used to make production decisions.

## Dataset and split
- Input dataset: `data/processed/Day5_Feature_Dataset_v2.csv`
- Dataset rows: 180
- Training rows: 135
- Test rows: 45
- Synthetic positive labels: 63
- Synthetic negative labels: 117
- Random seed: 42
- Train/test split: 75% / 25%, stratified

## Model features
Industry / Sub-industry, Target Customers / B2B or B2C, Founded Year (Standardized), Employee Count (Numeric), Company Age (Years)

Company names, pre-existing score fields, and data-quality flags were excluded from model inputs.

## Model comparison
All metrics use the held-out synthetic test set and a 0.50 demonstration threshold.

| Model | Accuracy | Balanced Accuracy | Precision | Recall | F1 | ROC_AUC | Average_Precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Random Forest | 0.6444 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | 0.6509 | 0.4845 |
| Random Forest Balanced | 0.6667 | 0.5873 | 0.5556 | 0.3125 | 0.4000 | 0.6325 | 0.4637 |
| Hist Gradient Boosting Balanced | 0.6444 | 0.5981 | 0.5000 | 0.4375 | 0.4667 | 0.6002 | 0.4706 |
| Hist Gradient Boosting | 0.6444 | 0.5560 | 0.5000 | 0.2500 | 0.3333 | 0.5744 | 0.4773 |
| Logistic Regression Balanced | 0.6000 | 0.4935 | 0.3333 | 0.1250 | 0.1818 | 0.5172 | 0.4222 |
| Logistic Regression | 0.6222 | 0.4968 | 0.3333 | 0.0625 | 0.1053 | 0.5172 | 0.4217 |

## Calibration assessment
Brier score and log loss are included as diagnostic measures. Calibration on random synthetic labels does not establish useful real-world probability estimates.

| Model | Brier Score | Log Loss | ROC_AUC | Average_Precision | Evaluation |
| --- | --- | --- | --- | --- | --- |
| Balanced Logistic Regression - Uncalibrated | 0.2425 | 0.6784 | 0.5172 | 0.4222 | Synthetic demonstration only |
| Balanced Logistic Regression - Sigmoid Calibrated | 0.2320 | 0.6572 | 0.5086 | 0.3850 | Synthetic demonstration only |

## Threshold analysis
No business threshold has been approved. Thresholds are shown for technical exploration only.

| Threshold | Precision | Recall | F1 | True Positives | False Positives | True Negatives | False Negatives | Predicted Positive Count | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.3000 | 0.3824 | 0.8125 | 0.5200 | 13 | 21 | 8 | 3 | 34 | Exploratory only; no approved business threshold |
| 0.4000 | 0.4000 | 0.1250 | 0.1905 | 2 | 3 | 26 | 14 | 5 | Exploratory only; no approved business threshold |
| 0.5000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 29 | 16 | 0 | Exploratory only; no approved business threshold |
| 0.6000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 29 | 16 | 0 | Exploratory only; no approved business threshold |
| 0.7000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 29 | 16 | 0 | Exploratory only; no approved business threshold |

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
