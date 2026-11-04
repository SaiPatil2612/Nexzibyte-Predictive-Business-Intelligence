# Day 9 - Margin Risk Report

## Status
Synthetic demonstration only; real-business validation pending.

## Method
Forecast gross margin = (Project Revenue - Forecast Delivery Cost)
/ Project Revenue.

Projects with forecast gross margin below 20% are flagged as high
margin risk. The 20% threshold is illustrative and pending finance
approval; it is not an approved NexziByte business rule.

## Test-set summary
- Test projects: 60
- Below the illustrative 20% margin threshold: 12
- At or above the illustrative 20% threshold: 48

## Model evaluation
The low-margin classifier performed poorly on the synthetic
time-separated test set. The previously recorded evaluation showed:
- Logistic Regression ROC-AUC: 0.3681
- Random Forest ROC-AUC: 0.4045

Neither model is recommended as a reliable margin-risk predictor.
These metrics describe the earlier synthetic evaluation and must
not be interpreted as real-business performance.

## Limitations
- Revenue and delivery costs are synthetic.
- The margin threshold requires finance approval.
- Margin risk in this register is rule-based, not a calibrated
  model probability.
- Actual delivery cost is an outcome field, not a predictor.
- No real project-level financial records were found in the
  audited datasets.

## Required validation
Obtain approved project revenue, forecast delivery costs, the
official gross-margin definition, and a finance-approved threshold.
Validate the margin calculations against real, dated project data
before considering operational use.
