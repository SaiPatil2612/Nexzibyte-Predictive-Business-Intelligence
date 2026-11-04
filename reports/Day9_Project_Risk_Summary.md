# Day 9 - Project Risk Summary

## Status
Synthetic demonstration complete; business validation pending.

## Evaluation design
- Total synthetic records: 300
- Training records: 240
- Test records: 60
- Split: chronological by project start date

## Test-set delay-risk register
- High delay-risk flags: 26
- Medium delay-risk flags: 25
- Low delay-risk flags: 9

## Test-set effort-overrun-risk register
- High effort-overrun-risk flags: 16
- Medium effort-overrun-risk flags: 17
- Low effort-overrun-risk flags: 27

## Test-set margin assessment
- Projects below the illustrative 20% forecast gross-margin threshold: 12
- Projects at or above the illustrative 20% threshold: 48

## Model selection
- Delay: Random Forest, based on the previously recorded higher
  synthetic test-set F1 score.
- Effort overrun: Logistic Regression, based on the previously
  recorded higher synthetic test-set F1 score.
- Low-margin classifier: not recommended due to previously recorded
  ROC-AUC below 0.50.

The delay and effort models were retrained by this code. The model
selection statements above refer to the earlier evaluation results;
rerun model evaluation if the dataset or split has changed.

## Risk classification
- High: probability >= 0.70
- Medium: probability >= 0.40 and < 0.70
- Low: probability < 0.40

These are provisional demonstration thresholds, not approved
operational business rules.

## Reason codes
Reason codes are transparent, rule-based indicators. They are not
SHAP explanations, causal findings, or proof of the cause of an outcome.

## Limitations and next steps
All records and outcomes are synthetic. Test metrics do not establish
real-world predictive performance. Verify cutoff-time availability,
obtain stakeholder approval for target definitions, and validate
against real dated project data before operational use.
