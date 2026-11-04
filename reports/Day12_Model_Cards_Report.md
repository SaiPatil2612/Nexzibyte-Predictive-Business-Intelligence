# Day 12 — Explainable AI and Model Governance

## 1. Purpose

Document model purpose, features, evaluation, explanations, limitations, intended use, prohibited use, and approval status.

## 2. Data and Governance Statement

**All models covered here use synthetic demonstration data.** The results do not establish real-world predictive performance. No model is approved for production use.

These model cards support technical evaluation and governance documentation. They do not establish that any model is suitable for real business decisions.

## 3. Lead Conversion Classification

- **Model ID:** DAY6_LEAD_MODEL
- **Purpose:** Demonstrate classification of synthetic lead-conversion labels.
- **Model type:** Logistic Regression
- **Features:** Industry / Sub-industry, Target Customers / B2B or B2C, Founded Year (Standardized), Employee Count (Numeric), Company Age (Years)
- **Target:** Synthetic_Lead_Conversion
- **Evaluation split:** Stratified random split, 75% train and 25% test, random_state=42.
- **Test records:** 45
- **Accuracy:** 0.6222
- **Precision:** 0.3333
- **Recall:** 0.0625
- **F1 score:** 0.1053
- **ROC-AUC:** 0.5172
- **PR-AUC:** 0.4217
- **Explanation method:** Preliminary group-level fairness analysis was conducted separately. A coefficient-based explanation summary has not been established in the current model card.
- **Calibration status:** Not assessed in the original Day 6 evaluation.
- **Fairness status:** Preliminary synthetic group-level evaluation completed; overall fairness validation pending.
- **Intended use:** Educational model evaluation and governance demonstration only.
- **Prohibited use:** Do not use to prioritize real leads, allocate sales resources, or predict actual customer conversion.
- **Limitations:** Synthetic labels and data; low recall in the original evaluation; no evidence of real-world predictive validity. The small test set limits confidence in the metrics.
- **Approval status:** Not approved for production use.

## 4. Quotation Win Classification

- **Model ID:** DAY7_QUOTE_LOGISTIC
- **Purpose:** Demonstrate classification of synthetic Won/Lost quotations.
- **Model type:** Logistic Regression
- **Features:** Quote_Value, Discount_Pct, Revision_Count, Engagement_Count
- **Target:** Won versus Lost; Pending quotations excluded.
- **Evaluation split:** Stratified random split, 80% train and 20% test, random_state=42.
- **Test records:** 51
- **Observed positive rate:** 0.4706
- **Mean predicted probability:** 0.4732
- **Brier score:** 0.2288
- **Log loss:** 0.6499
- **Explanation method:** Standardized logistic regression coefficients.
- **Top explanation features by absolute value:** Discount_Pct, Engagement_Count, Revision_Count, Quote_Value.
- **Calibration status:** Exploratory check completed; reliability not established.
- **Fairness status:** Not fully assessed; company-attribute mapping requires verification before group-level evaluation.
- **Intended use:** Educational evaluation and model-governance demonstration only.
- **Prohibited use:** Do not use to approve discounts, prioritize real quotations, or forecast actual sales.
- **Limitations:** Synthetic data and outcomes; no evidence of real-world validity. Coefficients describe model associations, not causal effects.
- **Approval status:** Not approved for production use.

## 5. Project Delay Risk

- **Model ID:** DAY9_PROJECT_DELAY_RF
- **Purpose:** Demonstrate classification of synthetic project-delay labels.
- **Model type:** Random Forest Classifier
- **Features:** Planned_Effort, Milestones_Planned, Milestones_Completed, Change_Request_Count, Dependency_Delay_Days, Client_Delay_Days, Resource_Utilization, Project_Age_Days_At_Cutoff
- **Target:** Project_Delayed
- **Evaluation split:** Chronological 80% train and 20% test split.
- **Test records:** 60
- **Observed positive rate:** 0.9167
- **Mean predicted probability:** 0.6532
- **Brier score:** 0.1405
- **Log loss:** 0.4441
- **Explanation method:** Random Forest impurity-based feature importance.
- **Top explanation features by importance:** Client_Delay_Days, Dependency_Delay_Days, Project_Age_Days_At_Cutoff, Planned_Effort, Change_Request_Count.
- **Calibration status:** Exploratory check completed; reliability not established.
- **Fairness status:** Pending approval of appropriate operational project comparison groups.
- **Intended use:** Educational risk-analysis and governance demonstration only.
- **Prohibited use:** Do not make real project staffing, escalation, or delivery decisions from these probabilities.
- **Limitations:** Synthetic data. The test positive rate is 91.67%, compared with a mean predicted probability of 65.32%. This difference warrants further investigation but does not, by itself, establish the cause of the calibration concern.
- **Approval status:** Not approved for production use.

## 6. Project Effort Overrun Risk

- **Model ID:** DAY9_EFFORT_OVERRUN_LOGISTIC
- **Purpose:** Demonstrate classification of synthetic effort-overrun labels.
- **Model type:** Logistic Regression
- **Features:** Planned_Effort, Milestones_Planned, Milestones_Completed, Change_Request_Count, Dependency_Delay_Days, Client_Delay_Days, Resource_Utilization, Project_Age_Days_At_Cutoff
- **Target:** Effort_Overrun
- **Evaluation split:** Chronological 80% train and 20% test split.
- **Test records:** 60
- **Observed positive rate:** 0.4500
- **Mean predicted probability:** 0.4433
- **Brier score:** 0.1481
- **Log loss:** 0.4442
- **Explanation method:** Standardized logistic regression coefficients.
- **Top explanation features by absolute value:** Resource_Utilization, Dependency_Delay_Days, Client_Delay_Days, Change_Request_Count, Milestones_Completed.
- **Calibration status:** Exploratory check completed; reliability not established.
- **Fairness status:** Pending definition and approval of appropriate operational project comparison groups.
- **Intended use:** Educational risk-analysis and governance demonstration only.
- **Prohibited use:** Do not use to estimate actual project costs, staffing requirements, or contractual exposure.
- **Limitations:** Synthetic data; coefficients represent model associations, not causal effects. Probability calibration is not established.
- **Approval status:** Not approved for production use.

## 7. Explainability Summary

The Day 12 explainability output contains 20 explanation records across three models:

1. DAY7_QUOTE_LOGISTIC
2. DAY9_PROJECT_DELAY_RF
3. DAY9_EFFORT_OVERRUN_LOGISTIC

Output file: `data/processed/Day12_Model_Explainability.csv`

Logistic regression coefficients describe associations within the fitted model. Random Forest impurity-based feature importance describes relative feature contributions to impurity reduction during training.

Neither explanation method establishes causation. SHAP-based explanations were not implemented in this assessment.

The Day 6 lead model was evaluated separately using group-level fairness metrics. A coefficient-based explanation summary for that model has not been established in this report.

## 8. Probability Calibration Summary

The exploratory calibration output is stored in:

`data/processed/Day12_Probability_Calibration_Checks.csv`

The results cover the quote, project delay, and effort-overrun models.

A close match between the overall mean predicted probability and observed positive rate does not, by itself, prove calibration. The project delay model's difference between its observed positive rate and mean predicted probability requires further investigation.

No calibration correction has been applied, and the current results do not establish production reliability.

## 9. Fairness Assessment Summary

Preliminary group-level fairness evaluation was conducted for the Day 6 lead model using its existing synthetic test predictions.

Outputs:

- `data/processed/Day12_Lead_Model_Group_Fairness.csv`
- `data/processed/Day12_Lead_Model_Customer_Type_Fairness.csv`

The industry assessment identified low recall in several groups. The customer-type assessment contained 44 groups from 45 records, making meaningful comparisons unreliable because most groups had only one record.

These results are exploratory and do not establish real-world fairness or discrimination.

The fairness assessment plan is stored in:

`data/processed/Day12_Fairness_Assessment_Plan.csv`

Overall fairness validation remains pending. Additional business-approved group definitions, sufficient observations, suitable data, and review are required.

## 10. Governance Requirements Before Real-World Use

1. Obtain verified, representative historical business data.
2. Confirm target definitions and feature availability at prediction time.
3. Evaluate performance on a suitable held-out dataset.
4. Investigate probability calibration, class imbalance, and relevant error rates.
5. Review fairness, data quality, privacy, and operational risks where applicable.
6. Validate model explanations and avoid causal interpretations.
7. Establish monitoring, drift detection, and retraining procedures.
8. Obtain business-owner approval and document monitoring responsibilities.
9. Record model versions, dependencies, data lineage, and reproducible evaluation procedures.
10. Document the intended use, prohibited uses, and conditions for withdrawal or review.

## 11. Day 12 Deliverables

### Processed data files

- `Day12_Model_Inventory.csv`
- `Day12_Model_Explainability.csv`
- `Day12_Probability_Calibration_Checks.csv`
- `Day12_Model_Cards.csv`
- `Day12_Experiment_Log.csv`
- `Day12_Reproducibility_Manifest.json`
- `Day12_Fairness_Assessment_Plan.csv`
- `Day12_Lead_Model_Group_Fairness.csv`
- `Day12_Lead_Model_Customer_Type_Fairness.csv`

Location: `data/processed/`

### Reports

- `Day12_Model_Cards_Report.md`
- `Day12_Explainable_AI_Governance_Report.md`
- `Day12_Fairness_Assessment_Report.md`

Location: `reports/`

## 12. Final Assessment

| Area | Status |
|---|---|
| Lead model evaluation documentation | Completed using existing synthetic evaluation metrics |
| Quote model card | Completed |
| Project delay model card | Completed |
| Effort overrun model card | Completed |
| Explainability documentation | Completed for three models |
| Probability calibration checks | Exploratory checks completed |
| Model inventory | Completed |
| Experiment log | Created |
| Reproducibility manifest | Created; full reproducibility not guaranteed |
| Preliminary lead-model fairness assessment | Completed using synthetic data |
| Overall fairness validation | Pending |
| Business validation | Pending |
| Production approval | Not granted |

## 13. Interpretation Warning

Model coefficients and feature importance describe how fitted models behave; they do not establish causation.

A close match between the overall mean predicted probability and observed outcome rate does not, by itself, prove calibration.

Group-level metric differences from small synthetic samples do not establish real-world discrimination or fairness.

All model metrics in this report are based on synthetic demonstration data and must not be presented as actual business performance.

**Final status: Day 12 model-card documentation completed; business validation and overall fairness validation pending. No model is approved for production use.**