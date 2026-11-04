# Day 6 — Lead Model Evaluation

## Data status
SYNTHETIC DEMONSTRATION ONLY. Outcome labels were randomly generated.
These metrics do not represent actual NexziByte lead-conversion performance.

## Dataset
- Total records: 180
- Training records: 135
- Test records: 45
- Input features: Industry / Sub-industry, Target Customers / B2B or B2C, Founded Year (Standardized), Employee Count (Numeric), Company Age (Years)
- Target: Synthetic_Lead_Conversion

## Logistic Regression baseline

| Metric | Value |
|---|---:|
| Accuracy | 0.6222 |
| Precision | 0.3333 |
| Recall | 0.0625 |
| F1-score | 0.1053 |
| ROC-AUC | 0.5172 |
| PR-AUC (Average Precision) | 0.4217 |

## Confusion matrix
Rows are actual labels [0, 1]; columns are predicted labels [0, 1].

[[27, 2], [15, 1]]

## Limitations
- No verified historical conversion outcome was available in the audited prospect dataset.
- Synthetic labels were randomly generated and do not represent real business outcomes.
- These metrics must not be used for sales decisions or presented as real model performance.
- A production lead propensity model requires a business-approved target definition,
  historical outcomes, an observation window, and a leakage-safe evaluation design.

## Outputs
- data/processed/Day6_Synthetic_Baseline_Metrics.csv
- data/processed/Day6_Synthetic_Scored_Output.csv
