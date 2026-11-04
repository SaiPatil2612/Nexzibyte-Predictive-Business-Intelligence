# Day 15 — Limitations and Recommendations

## 1. Project Overview

Project: NexziByte Predictive Business Intelligence & Growth Engine

Purpose: Document the known limitations of the analytical, predictive, dashboard and API prototype and identify recommended next steps.

## 2. Data Limitations

1. The cleaned prospect dataset contains 180 records.
2. Verified prospect conversion outcomes were unavailable.
3. Historical engagement time-series data was unavailable.
4. Historical quotation records and verified quotation outcomes were unavailable.
5. Several predictive demonstrations use synthetic datasets.
6. Synthetic records do not represent actual NexziByte customer behavior.

### Recommendations

- Collect verified historical prospect and quotation records.
- Maintain consistent customer and company identifiers.
- Record quotation dates, values, discounts and outcomes.
- Maintain historical engagement information.
- Establish approved data definitions and data-quality controls.

## 3. Model Limitations

### Prospect Conversion

- Day 5 baseline conversion modeling was blocked because verified conversion labels were unavailable.
- Existing prospect scores must not be treated as observed conversion outcomes.

### Quotation Win Classification

- Day 7 Logistic Regression was trained using synthetic quotation data.
- Test-set accuracy was 58.82%.
- Test-set ROC-AUC was 0.6620.
- The model achieved 58.82% accuracy against a 52.94% majority-class baseline.
- These metrics apply only to the synthetic test dataset.

### Revenue Forecasting

- Revenue forecasting demonstrations use synthetic monthly revenue data.
- Forecast outputs depend on illustrative assumptions and should not be interpreted as actual business forecasts.

### Recommendations

- Retrain models using verified historical business data.
- Validate target definitions with business stakeholders.
- Perform time-aware validation where appropriate.
- Assess model calibration and business usefulness.
- Monitor model performance after deployment.

## 4. Dashboard Limitations

- The Power BI executive dashboard has been completed.
- Service-category performance analysis has a documented limitation because standardized Service_Category and prospect-to-quotation mapping were unavailable.
- Dashboard metrics require business-owner validation before operational decisions are based on them.

### Recommendations

- Standardize service-category values.
- Establish prospect-to-quotation relationships.
- Validate KPI calculations with business stakeholders.
- Establish a dashboard refresh and ownership process.

## 5. API and Integration Limitations

- The FastAPI quotation prediction endpoint works as a local prototype.
- The API uses synthetic demonstration data.
- Authentication and authorization have not been implemented.
- Production deployment and live business-system integration have not been completed.
- A non-blocking Starlette deprecation warning remains in the test environment concerning httpx and TestClient.

### Recommendations

- Implement authentication and authorization before production deployment.
- Define secure API key and secrets management.
- Add production logging and monitoring.
- Review deployment and infrastructure requirements.
- Resolve dependency deprecation warnings during future maintenance.

## 6. Governance and Business Limitations

- Business KPI validation remains pending.
- The proposed 90-day quotation acceptance window requires business confirmation.
- Real-world model validation remains pending.
- Business acceptance and production approval have not been obtained.

### Recommendations

- Obtain formal approval of KPI and target definitions.
- Document data ownership and access permissions.
- Review fairness, explainability and governance controls.
- Establish a model review and approval process.
- Assign business and technical owners for ongoing monitoring.

## 7. Security and Operational Readiness

Before production use, the project requires:

1. Authentication and authorization.
2. Secure configuration and secrets management.
3. Data privacy and access controls.
4. Deployment and backup procedures.
5. Error handling and operational monitoring.
6. Model versioning and rollback procedures.
7. Documented maintenance responsibilities.

## 8. Recommended Next-Phase Roadmap

### Phase 1 — Business Data Readiness

- Obtain historical business datasets.
- Validate KPI and outcome definitions.
- Establish data ownership and refresh processes.

### Phase 2 — Predictive Model Validation

- Retrain using verified historical outcomes.
- Compare against appropriate business baselines.
- Evaluate model performance and calibration.
- Conduct business acceptance testing.

### Phase 3 — Production Engineering

- Secure and deploy the prediction API.
- Implement monitoring and logging.
- Integrate approved data sources.
- Establish model version control.

### Phase 4 — Business Adoption

- Validate Power BI metrics with stakeholders.
- Define operational workflows.
- Train intended users.
- Monitor business impact and model performance.

## 9. Final Conclusion

The project demonstrates an end-to-end predictive business intelligence prototype using analytical workflows, synthetic predictive models, Power BI dashboards and a FastAPI integration.

The main limitations relate to the availability of verified historical business outcomes, synthetic model training data, pending business validation and production-readiness requirements.

The recommended next phase should prioritize business data readiness, real-world model validation, governance and secure production engineering.

**Final status:** Technical demonstration completed for the documented scope. Business validation and production approval pending.