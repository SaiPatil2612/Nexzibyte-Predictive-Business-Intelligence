# NexziByte Predictive Business Intelligence & Growth Engine
## Final Technical Report

**Project Duration:** 15 Days  
**Project Type:** Data Science Internship Project  
**Organization:** NexziByte  
**Final Review Date:** 5 November 2026  
**Project Status:** Technical demonstration completed; business validation pending.

---

## 1. Executive Summary

The NexziByte Predictive Business Intelligence & Growth Engine project demonstrates an end-to-end business intelligence and predictive analytics workflow.

The project covers business requirements documentation, data preparation, exploratory analysis, feature engineering, predictive modeling, forecasting, risk analysis, customer intelligence, explainable AI, dashboard development and API integration.

A Power BI executive dashboard and a FastAPI quotation prediction prototype were developed.

The project also includes automated testing, model benchmarking, governance documentation and recommendations for future production implementation.

Several predictive workflows use synthetic demonstration data because verified historical business outcomes were not available.

## 2. Project Objectives

1. Understand and document business processes and KPIs.
2. Prepare and validate analytical datasets.
3. Perform exploratory data analysis.
4. Engineer features for predictive analytics.
5. Demonstrate lead and quotation scoring workflows.
6. Develop revenue forecasting and risk analysis demonstrations.
7. Generate customer intelligence and recommendations.
8. Document explainability, fairness and model governance.
9. Develop an executive Power BI dashboard.
10. Expose selected model predictions through an API.
11. Test the integrated prototype and document limitations.

## 3. Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Data processing | Pandas |
| Machine learning | Scikit-learn |
| Model serialization | Joblib |
| API development | FastAPI |
| API server | Uvicorn |
| Data validation | Pydantic |
| Automated testing | Pytest |
| Visualization and BI | Power BI |
| Data storage | CSV and structured project files |
| Development | VS Code, Conda |

## 4. Fifteen-Day Project Execution Summary

### Day 1 — Business Requirements and Project Charter

- Prepared BRD-lite documentation.
- Prepared project charter.
- Developed KPI dictionary.
- Documented target definitions and success criteria.
- Created business process map.

Status: Documentation complete; business validation pending.

### Day 2 — Analytical Dimensional Model

- Prepared analytical dimensional model.
- Documented data structures and relationships.
- Completed documented QA corrections.

Status: Documentation completed.

### Day 3 — Data Preparation and ETL

- Implemented data cleaning and validation workflows.
- Created ETL validation tests.
- Documented data quality findings.

Status: Technical implementation and automated tests completed.

### Day 4 — Exploratory Data Analysis

- Examined available business data.
- Documented exploratory findings.
- Identified data patterns and limitations.

Status: Completed.

### Day 5 — Feature Engineering and Baseline Readiness

- Generated a 180-record feature dataset with 19 columns.
- Prepared feature catalogue.
- Completed baseline readiness assessment.
- Verified source data integrity.

Status: Feature engineering completed. Prospect conversion baseline modeling remained blocked because verified conversion outcomes were unavailable.

### Day 6 — Lead Scoring Demonstration

- Developed an enhanced lead scoring demonstration.
- Generated scored outputs and priority queues.
- Prepared threshold and calibration assessments.

Status: Synthetic demonstration completed.

### Day 7 — Quotation Win Classification

- Generated 300 synthetic quotation records.
- Excluded pending quotations from binary modeling.
- Developed Logistic Regression model.
- Evaluated the model using a held-out test set.
- Prepared driver analysis and leakage documentation.

Model evaluation:
- Accuracy: 58.82%
- Won precision: 57.14%
- Won recall: 50.00%
- Won F1-score: 53.33%
- ROC-AUC: 66.20%

Status: Synthetic demonstration completed; real-world validation pending.

### Day 8 — Revenue Forecasting

- Developed revenue forecasting demonstrations.
- Prepared naive and linear trend comparisons.
- Generated forward revenue scenarios.
- Documented forecasting assumptions.

Status: Synthetic forecasting demonstration completed.

### Day 9 — Margin and Project Risk

- Prepared synthetic project risk analysis.
- Documented margin and project risk findings.

Status: Demonstration completed.

### Day 10 — Customer Intelligence

- Developed customer intelligence analysis.
- Prepared supporting analytical documentation.

Status: Completed.

### Day 11 — Recommendations and Anomaly Detection

- Developed recommendation and anomaly detection demonstrations.
- Prepared supporting reports.

Status: Completed.

### Day 12 — Explainable AI and Governance

- Prepared model cards.
- Documented fairness assessment.
- Prepared explainable AI and governance documentation.

Status: Documentation completed; business validation pending.

### Day 13 — Power BI Executive Dashboard

Developed a seven-page executive dashboard:

1. Executive Command Center
2. Sales Intelligence
3. Proposal Intelligence
4. Project Health
5. Customer 360
6. Forecast & Scenarios
7. Data & Model Health

Dashboard artifact:

`powerbi/NexziByte_Executive_Dashboard.pbix`

Status: Dashboard completed. Standardized service-category and prospect-to-quotation mapping limitations remain documented.

### Day 14 — API Prototype and Integration

- Developed FastAPI quotation prediction endpoint.
- Implemented request validation.
- Prepared API contract.
- Created automated API tests.
- Generated sample prediction CSV.
- Prepared integration documentation.

Main files:

- `api/main.py`
- `api/test_api.py`
- `api/export_predictions.py`
- `api/Day14_API_Contract.md` is stored under `docs/Day14_API_Contract.md`.
- `docs/Day14_Integration_Note.md`

Status: Prototype and documentation completed.

### Day 15 — Final Validation and Handover Preparation

- Audited project structure and deliverables.
- Executed complete automated test suite.
- Tested live API prediction endpoint.
- Tested live API validation behavior.
- Compared Logistic Regression against a majority-class baseline.
- Prepared business acceptance review.
- Documented limitations and recommendations.

Status: Technical validation and documentation completed; final package and handover preparation in progress.

## 5. Model Evaluation and Benchmarking

The Day 7 quotation model was evaluated against a majority-class baseline.

| Metric | Logistic Regression | Majority Baseline |
|---|---:|---:|
| Accuracy | 58.82% | 52.94% |
| Won precision | 57.14% | 0.00% |
| Won recall | 50.00% | 0.00% |
| Won F1-score | 53.33% | 0.00% |
| ROC-AUC | 66.20% | 50.00% |

Both models were evaluated on the same 51 synthetic test records.

The Logistic Regression model performed better than the majority baseline on this evaluation dataset.

These metrics do not establish real-world quotation prediction performance because the training and test data are synthetic.

## 6. API Integration Results

Prediction endpoint:

`POST /api/v1/predict/quotation`

Model identifier:

`DAY7_QUOTE_LOGISTIC`

Input features:

- Quote_Value
- Discount_Pct
- Revision_Count
- Engagement_Count

The live API returned the expected prediction response for the tested quotation.

Input validation also correctly rejected an invalid zero quotation value with HTTP 422.

The API explicitly identifies its outputs as synthetic demonstration results and states that production approval has not been granted.

## 7. Automated Testing Results

Full project test execution:

`python -m pytest -v`

Results:

- API tests: 9 passed.
- ETL tests: 13 passed