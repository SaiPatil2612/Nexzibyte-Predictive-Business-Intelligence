# Day 15 — Quotation Model vs Baseline Comparison

## 1. Executive Summary

The Day 7 Logistic Regression quotation model was compared against a simple Majority Class Baseline using the same synthetic test dataset.

The Logistic Regression model achieved 58.82% accuracy and 0.662 ROC-AUC, compared with 52.94% accuracy and 0.500 ROC-AUC for the majority-class baseline.

The results demonstrate better classification performance than the simple baseline on this synthetic test set. They do not establish real-world business performance or production readiness.

## 2. Dataset and Evaluation Method

- Dataset: `data/synthetic/Day7_Synthetic_Quote_Modeling_Dataset.csv`
- Total modeling records: 255
- Won records: 118
- Lost records: 137
- Training records: 204
- Testing records: 51
- Split: Stratified train/test split
- Random state: 42
- Test size: 20%

Both models were evaluated on the same test records.

## 3. Models Compared

### Logistic Regression

- Model ID: `DAY7_QUOTE_LOGISTIC`
- Algorithm: Logistic Regression
- Preprocessing: StandardScaler
- Input features:
  - Quote_Value
  - Discount_Pct
  - Revision_Count
  - Engagement_Count

The previously saved model artifact was loaded for evaluation. It was not retrained.

### Majority Class Baseline

- Algorithm: DummyClassifier
- Strategy: `most_frequent`
- Training data: Same training split
- Prediction behavior: Always predicts the majority training class.

## 4. Comparison Results

| Metric | Logistic Regression | Majority Class Baseline |
|---|---:|---:|
| Test records | 51 | 51 |
| Accuracy | 0.5882 | 0.5294 |
| Won precision | 0.5714 | 0.0000 |
| Won recall | 0.5000 | 0.0000 |
| Won F1-score | 0.5333 | 0.0000 |
| ROC-AUC | 0.6620 | 0.5000 |

## 5. Key Findings

1. Logistic Regression achieved 58.82% accuracy.
2. The majority-class baseline achieved 52.94% accuracy.
3. Logistic Regression improved accuracy by approximately 5.88 percentage points.
4. Logistic Regression achieved a Won F1-score of 0.5333.
5. The majority baseline predicted all test records as Lost and therefore had zero Won precision and recall.
6. Logistic Regression achieved a ROC-AUC of 0.6620, compared with 0.5000 for the baseline.

## 6. Interpretation

The Logistic Regression model performed better than the simple majority-class benchmark across the reported metrics.

However, this evaluation uses synthetic quotation records and artificially generated outcomes. The metrics describe performance on the held-out synthetic test set only.

They must not be interpreted as evidence of actual quotation conversion performance at NexziByte.

## 7. Limitations

- No verified historical quotation records were available.
- Won and Lost outcomes were synthetic.
- The test set contained only 51 records.
- Synthetic data generation may introduce artificial patterns that the model learns.
- No business acceptance or production validation has been completed.
- Performance may differ substantially on real quotation data.

## 8. Recommendations

1. Obtain historical quotation records linked to company IDs.
2. Validate quotation outcome definitions with the business owner.
3. Confirm the proposed 90-day acceptance window.
4. Retrain and evaluate using verified historical data.
5. Assess probability calibration and business usefulness.
6. Obtain business approval before any production deployment.

## 9. Output Artifact

Comparison results:

`reports/Day15_Quote_Model_vs_Baseline.csv`

Comparison script:

`api/compare_quote_baseline.py`

Original dataset and saved Logistic Regression model were not modified.

## 10. Conclusion

The Day 7 Logistic Regression model outperformed the majority-class baseline on the synthetic evaluation dataset.

The comparison completes the technical demonstration of model benchmarking for Day 15. Real-world model validation remains pending until verified historical quotation data and business-approved target definitions become available.

**Data classification:** Synthetic demonstration only.

**Production approval:** Not approved.