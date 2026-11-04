
# Day 14 — Integration Prototype & Scenario Testing Note

## 1. Project Information

- Project: NexziByte Predictive Business Intelligence & Growth Engine
- Day: 14
- Integration: Quotation Win Prediction API
- Model ID: DAY7_QUOTE_LOGISTIC
- Status: Prototype implementation completed; documentation and final validation pending

## 2. Objective

Expose the selected quotation prediction model through a REST API, demonstrate a JSON request/response contract, export sample predictions for Power BI integration, and validate normal and edge-case scenarios.

## 3. Integration Architecture

The prototype follows this flow:

1. Client submits quotation information as JSON.
2. FastAPI receives and validates the request.
3. The saved Logistic Regression pipeline loads the quotation features.
4. The model generates Won/Lost predictions and probabilities.
5. The API returns a structured JSON response.
6. Sample predictions can be exported as CSV for Power BI.

## 4. Technical Components

| Component | Technology |
|---|---|
| API framework | FastAPI |
| API server | Uvicorn |
| Model | Logistic Regression |
| Preprocessing | StandardScaler |
| Model loading | Joblib |
| Data processing | Pandas |
| Validation | Pydantic |
| Automated testing | Pytest |
| Integration output | CSV |

## 5. Model Artifact

Model identifier: DAY7_QUOTE_LOGISTIC

Artifact location:

notebooks/models/Day7_Quote_Logistic_Model.joblib

Input features:

- Quote_Value
- Discount_Pct
- Revision_Count
- Engagement_Count

Target:

- Won_Flag (Won = 1, Lost = 0)

## 6. API Integration

Prediction endpoint:

POST /api/v1/predict/quotation

Local API address:

http://127.0.0.1:8000

Interactive documentation:

http://127.0.0.1:8000/docs

Health endpoint verification:

GET /health

Verified response:

{
  "status": "healthy",
  "model_loaded": true
}

## 7. Scenario Testing Results

### Manual API tests

| Scenario | Expected HTTP Status | Result |
|---|---:|---|
| Valid quotation request | 200 | Passed |
| Boundary values | 200 | Passed |
| Zero quotation value | 422 | Passed |
| Discount above 100% | 422 | Passed |
| Negative revision count | 422 | Passed |
| Negative engagement count | 422 | Passed |
| Unexpected additional field | 422 | Passed |
| Missing required field | 422 | Passed |

### Automated tests

Test file:

api/test_api.py

Result:

9 tests passed.

One non-blocking Starlette deprecation warning remains concerning the use of httpx with TestClient. It does not affect the successful test results.

## 8. Sample Prediction Export

Export script:

api/export_predictions.py

Generated file:

data/processed/Day14_API_Sample_Predictions.csv

Records exported: 5

All five records were checked. Each record's win and lost probabilities sum to 1.0.

The CSV can be imported into Power BI for demonstration and integration testing.

The original dataset was not modified.

## 9. Observations and Risks

- The API successfully loads the saved model and generates predictions.
- Input validation rejects invalid and unexpected request fields.
- The boundary scenario with quote value 1 and discount 100% produced a Won prediction with approximately 0.998328 win probability.
- This unusual boundary result demonstrates that model outputs should not be interpreted as business rules or guaranteed outcomes.
- The model and sample data are synthetic demonstration materials.
- Business validation and production approval remain pending.

## 10. Known Limitations

1. Synthetic demonstration data only.
2. No production authentication or authorization.
3. No production deployment.
4. No live business-system integration.
5. Model probabilities require further validation.
6. No business acceptance approval has been established.

## 11. Day 14 Deliverables

| Deliverable | Location | Status |
|---|---|---|
| FastAPI prototype | api/main.py | Implemented |
| API test suite | api/test_api.py | 9 tests passed |
| Prediction export script | api/export_predictions.py | Executed |
| Sample prediction CSV | data/processed/Day14_API_Sample_Predictions.csv | Generated |
| API contract | docs/Day14_API_Contract.md | Documented |
| Integration note | docs/Day14_Integration_Note.md | In progress |

## 12. Conclusion

The quotation prediction model has been exposed through a working FastAPI prototype. The JSON contract, input validation, manual scenarios, automated tests, and CSV prediction export have been demonstrated.

The prototype is suitable for project demonstration and further integration testing. It is not approved for production use.

Day 15 will focus on end-to-end testing, model-versus-baseline comparison, business acceptance review, limitations, final technical documentation, and handover.
