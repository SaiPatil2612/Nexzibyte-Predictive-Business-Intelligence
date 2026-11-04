# Day 12 — Explainable AI and Model Governance

## 1. Status

**Technical deliverables completed; business validation pending.**

The Day 12 technical work covers model inventory, explainability, exploratory probability calibration, model cards, experiment tracking, reproducibility documentation, and preliminary fairness assessment.

All evaluated model datasets and labels are synthetic. The results are intended for technical exploration and documentation, not as evidence of real-world business performance.

No model is approved for production use.

## 2. Scope

The work covers:

- Model inventory and documentation.
- Logistic regression coefficient analysis.
- Random Forest feature-importance analysis.
- Exploratory probability calibration checks.
- Model cards documenting purpose, features, evaluation, limitations, and intended use.
- Experiment logging and reproducibility documentation.
- Preliminary group-level fairness assessment for the synthetic lead model.
- Governance limitations and outstanding validation requirements.

SHAP was not installed during the environment inventory. The current explainability work uses model coefficients and Random Forest feature importance rather than SHAP-based explanations.

## 3. Explainability

### 3.1 Summary

- Explanation records generated: **20**
- Models represented in the explanation file: **3**
- Explanation output: `data/processed/Day12_Model_Explainability.csv`

The explanation file contains coefficient records for logistic regression models and feature-importance records for the Random Forest model.

### 3.2 Interpretation

**Logistic regression coefficients**

Coefficients describe associations between input features and the model's predicted outcome, conditional on the fitted model and its feature representation. They should not be interpreted as proof of causation or as evidence that changing a feature will produce a particular business outcome.

**Random Forest feature importance**

Impurity-based feature importance describes how much features contribute to the model's impurity reductions during training. It is a measure of relative model reliance, not a causal explanation. Correlated features and other properties of the training data can affect these values.

### 3.3 Limitations

- The evaluated datasets are synthetic.
- Explanations describe model behavior on the available synthetic data.
- Coefficients and feature importance do not establish causal relationships.
- SHAP-based explanations were not implemented in this assessment.
- Explanation results require additional review before being used to justify real business decisions.

## 4. Probability Calibration

Exploratory probability calibration checks were performed for three models.

### 4.1 Summary of Results

| Model | Test records | Observed positive rate | Mean predicted probability | Brier score | Log loss |
|---|---:|---:|---:|---:|---:|
| DAY7_QUOTE_LOGISTIC | 51 | 0.4706 | 0.4732 | 0.2288 | 0.6499 |
| DAY9_PROJECT_DELAY_RF | 60 | 0.9167 | 0.6532 | 0.1405 | 0.4441 |
| DAY9_EFFORT_OVERRUN_LOGISTIC | 60 | 0.4500 | 0.4433 | 0.1481 | 0.4442 |

Output file: `data/processed/Day12_Probability_Calibration_Checks.csv`

### 4.2 Interpretation

For the quote and effort-overrun models, the overall observed positive rates are relatively close to the corresponding mean predicted probabilities.

However, agreement between these overall averages does not prove that individual predictions are calibrated. Calibration should also be examined across probability ranges and, where appropriate, on suitable independent data.

The Brier score and log loss summarize aspects of probabilistic prediction quality. Neither metric alone establishes that a model is well calibrated.

### 4.3 Project Delay Calibration Concern

For `DAY9_PROJECT_DELAY_RF`, the observed positive rate was **0.9167**, while the mean predicted probability was **0.6532**.

This difference warrants further investigation. It indicates that the average predicted probability was substantially below the observed positive rate in the evaluated synthetic test set.

The result does not, by itself, identify the cause of the difference or establish production calibration performance.

No calibration correction has been applied. Further investigation would require reviewing the synthetic target distribution, test split, predicted probabilities, and calibration behavior across probability ranges.

### 4.4 Calibration Limitations

- All evaluated data and labels are synthetic.
- The results are exploratory.
- Overall average agreement is insufficient to establish calibration.
- The current checks do not establish real-world performance.
- No calibration correction or production approval has been applied.

## 5. Fairness Assessment

### 5.1 Overall Status

**Preliminary lead-model group evaluation completed; overall fairness validation pending.**

The assessment used existing test predictions from the Day 6 synthetic lead model. Group-level results were generated for Industry / Sub-industry and customer type.

The evaluation is exploratory and does not establish fairness or discrimination in real business operations.

### 5.2 Industry / Sub-industry Assessment

Output file: `data/processed/Day12_Lead_Model_Group_Fairness.csv`

The assessment covered seven industry/sub-industry groups in a synthetic test set containing 45 records.

Key observations:

- **AI / ML / GenAI:** 14 records; recall was 0.00, with four false negatives.
- **B2B SaaS / Enterprise Software:** 14 records; recall was 0.00, with five false negatives.
- **FinTech / Payments:** 13 records; recall was 0.25, with three false negatives and one false positive.
- The remaining three groups contained only one record each, making their group-level metrics unsuitable for reliable comparison.

These observations identify areas for further technical investigation. They do not establish that the model discriminates unfairly against any real-world industry.

### 5.3 Customer-Type Assessment

Output file: `data/processed/Day12_Lead_Model_Customer_Type_Fairness.csv`

The assessment produced 44 customer-type groups from 45 test records. Nearly all groups contained only one record.

The resulting metrics are too unstable and granular to support meaningful customer-type comparisons. Additional observations and a business-approved grouping strategy are required before interpreting group differences.

### 5.4 Fairness Limitations

- The lead dataset and labels are synthetic.
- The test set contains only 45 records.
- Most customer-type groups have insufficient observations for stable metrics.
- Small groups can produce extreme or undefined error rates.
- No protected-group fairness conclusion has been established.
- The quotation dataset requires verified data mapping before company attributes can be joined.
- Suitable project-risk comparison groups have not yet been approved.
- Business review and additional validation remain necessary.

### 5.5 Outstanding Fairness Actions

1. Approve comparison groups and evaluation criteria.
2. Define appropriate minimum sample sizes.
3. Investigate low recall in the lead-model industry groups.
4. Verify links between test predictions and original records.
5. Obtain suitable, authorized data for any real-world fairness review.
6. Complete quotation and project-risk assessments when suitable data and group definitions are available.
7. Obtain business-owner review before drawing operational conclusions.

## 6. Model Cards

Model cards were generated for the following models:

- `DAY7_QUOTE_LOGISTIC`
- `DAY9_PROJECT_DELAY_RF`
- `DAY9_EFFORT_OVERRUN_LOGISTIC`

Files:

- `data/processed/Day12_Model_Cards.csv`
- `reports/Day12_Model_Cards_Report.md`

The model cards document the models' purposes, features, targets, evaluation information, explanation methods, limitations, intended uses, prohibited uses, and governance status.

**Approval status:** All three documented models are not approved for production use.

The model cards are documentation artifacts, not evidence that the models have been validated for real business decisions.

## 7. Experiment Tracking and Reproducibility

### 7.1 Experiment Log

The experiment log contains **five records** documenting the Day 12 explainability, calibration, and governance work.

File:

`data/processed/Day12_Experiment_Log.csv`

### 7.2 Reproducibility Manifest

The reproducibility manifest records source dataset checksums and software-version information to support traceability.

File:

`data/processed/Day12_Reproducibility_Manifest.json`

### 7.3 Reproducibility Limitations

The manifest supports source-data identification and traceability, but the available documentation does not guarantee bit-for-bit reproduction of every experiment.

Full reproducibility would require complete executable experiment code, consistent dependencies, recorded random seeds and data splits, and verification that the recorded inputs and procedures match the generated outputs.

## 8. Data and Governance Limitations

- All evaluated datasets and labels are synthetic.
- Real historical business outcomes are required for real-world model validation.
- No model is approved for production.
- Business owners must validate targets, thresholds, assumptions, and intended use.
- Calibration requires further investigation and validation.
- Fairness assessment remains incomplete.
- Data privacy, access control, and authorized data use require review before any real-world evaluation.
- Operational monitoring, model drift checks, and retraining procedures must be designed before production deployment.
- Model explanations must not be presented as causal evidence.
- Synthetic performance metrics must not be represented as actual business performance.

## 9. Deliverables

### 9.1 Processed Data Files

1. `Day12_Model_Inventory.csv`
2. `Day12_Model_Explainability.csv`
3. `Day12_Probability_Calibration_Checks.csv`
4. `Day12_Model_Cards.csv`
5. `Day12_Experiment_Log.csv`
6. `Day12_Reproducibility_Manifest.json`
7. `Day12_Fairness_Assessment_Plan.csv`
8. `Day12_Lead_Model_Group_Fairness.csv`
9. `Day12_Lead_Model_Customer_Type_Fairness.csv`

All processed data files are located in:

`data/processed/`

### 9.2 Reports

1. `Day12_Model_Cards_Report.md`
2. `Day12_Explainable_AI_Governance_Report.md`
3. `Day12_Fairness_Assessment_Report.md`

All reports are located in:

`reports/`

## 10. Final Day 12 Assessment

| Area | Status |
|---|---|
| Model inventory | Completed |
| Coefficient and feature-importance explanations | Completed |
| Exploratory probability calibration checks | Completed |
| Model cards | Completed |
| Experiment log | Completed |
| Reproducibility manifest | Created; reproducibility limitations documented |
| Lead-model preliminary group assessment | Completed using synthetic data |
| Overall fairness validation | Pending |
| Business validation | Pending |
| Production approval | Not granted |

## 11. Conclusion

The Day 12 technical deliverables have been created for explainability, exploratory calibration, model documentation, experiment tracking, reproducibility support, and preliminary fairness assessment.

The project delay model's difference between observed positive rate and mean predicted probability warrants further investigation. The lead-model fairness assessment also identified low recall in several synthetic industry groups, while customer-type groups were too small for meaningful comparison.

These results are diagnostic findings from synthetic data, not evidence of real-world model performance, fairness, or business impact.

**Final status: Day 12 technical deliverables completed; business validation and overall fairness validation pending. No model is approved for production use.**