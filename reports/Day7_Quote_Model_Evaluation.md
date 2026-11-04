# Day 7 — Quotation Win Model Evaluation

## 1. Executive Summary

A baseline Logistic Regression model was developed using synthetic
quotation data for technical demonstration only.

No real quotation-level records or verified win/loss outcomes were
available in the supplied raw and cleaned prospect datasets.
Therefore, this is not a validated NexziByte business model.

## 2. Data Readiness

- Raw prospect records: 180
- Cleaned prospect records: 180
- Available quotation records: None identified
- Verified real quotation outcomes: Unavailable
- Business validation of target rules: Pending

## 3. Synthetic Dataset

- Synthetic quotations generated: 300
- Won: 118
- Lost: 137
- Pending: 45
- Records used for binary modeling: 255
- Training records: 204
- Testing records: 51

Pending quotations were excluded from binary modeling.

## 4. Features

- Quote_Value
- Discount_Pct
- Revision_Count
- Engagement_Count

The outcomes and features are synthetic. The dataset does not represent
actual NexziByte quotations or observed customer behavior.

## 5. Baseline Model

- Algorithm: Logistic Regression
- Test records: 51
- Accuracy: 0.5882
- Won precision: 0.5714
- Won recall: 0.5000
- Won F1 score: 0.5333
- ROC-AUC: 0.6620

These metrics evaluate predictions on a held-out synthetic test set only.

## 6. Driver Analysis

The fitted model's standardized coefficients indicate the direction and
relative magnitude of associations learned from the synthetic dataset.
They must not be interpreted as verified business drivers.

See:
- data/synthetic/Day7_Synthetic_Quote_Driver_Analysis.csv

## 7. Win-Probability Output

The test-set probability table contains 51 quotations.

See:
- data/synthetic/Day7_Synthetic_Quote_Win_Probability.csv

Predicted probabilities are demonstration outputs, not real-world
quotation win probabilities.

## 8. Limitations and Risks

1. No historical quotation records were available.
2. No verified acceptance or loss labels were available.
3. Quote values, discounts, revisions, engagement histories, and loss
   reasons were not available as real quotation features.
4. Target definitions require business validation, including the
   proposed 90-day acceptance window.
5. Synthetic outcomes were generated using an illustrative probability
   mechanism; the model can learn that artificial mechanism.
6. Performance metrics cannot establish production readiness.
7. Loss-reason records are synthetic and cannot establish actual
   quotation win/loss reasons.

## 9. Recommended Next Steps

1. Request historical quotations linked to company IDs.
2. Obtain quote dates, values, discounts, revision counts, and
   engagement history where available.
3. Confirm accepted, lost, and pending status definitions with the
   business owner.
4. Confirm the proposed 90-day acceptance window and required evidence.
5. Record genuine loss reasons where available.
6. Retrain and evaluate using verified historical data.
7. Validate probability calibration and business usefulness before
   production deployment.

## 10. Conclusion

The synthetic workflow demonstrates data preparation, train/test
splitting, Logistic Regression, evaluation, probability generation,
and coefficient analysis.

A real quotation win model remains blocked until verified historical
quotation data and business-approved target definitions are available.

**Data classification: Synthetic demonstration only.**


## 11. Leakage Audit

The leakage audit is saved at:
- data/processed/Day7_Quote_Model_Leakage_Audit.csv

Key controls:
- Quote_Status, Accepted_Date, and Loss_Reason must not be model inputs.
- Revision and engagement features must be limited to information
  available at the prediction cutoff.
- Synthetic outcome generation limits the interpretation of all metrics.

This is a documented risk audit, not proof that every possible leakage
risk has been eliminated.

## 12. Prediction Reason Codes

The rule-based synthetic reason-code output is saved at:
- data/synthetic/Day7_Synthetic_Quote_Reason_Codes.csv

Reason codes refer to illustrative input thresholds and coefficient
directions. They are not causal explanations, verified business
drivers, or SHAP explanations.

## 13. Final Day 7 Status

Synthetic demonstration workflow: completed.

Real quotation win model: blocked pending verified historical quotation
data and business-approved target definitions.

Business validation: pending, including confirmation of the proposed
90-day acceptance window.

All synthetic outputs must remain clearly identified as demonstration
artifacts and must not be presented as actual NexziByte results.
