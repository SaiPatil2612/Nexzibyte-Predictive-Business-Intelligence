
# Day 14 — Quotation Prediction API Contract

## 1. Project Information

- Project: NexziByte Predictive Business Intelligence & Growth Engine
- API: NexziByte Predictive BI API
- API Version: 1.0.0
- Model ID: DAY7_QUOTE_LOGISTIC
- Model: Logistic Regression Pipeline
- Dataset: Synthetic demonstration only
- Production Approval: Not approved

## 2. API Base URL

Local development:

http://127.0.0.1:8000

## 3. Available Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | API information |
| GET | /health | Health and model status |
| POST | /api/v1/predict/quotation | Quotation prediction |

## 4. Prediction Request Contract

Endpoint:

POST /api/v1/predict/quotation

Content-Type:

application/json

Request fields:

| Field | Type | Validation |
|---|---|---|
| quote_value | float | Greater than 0 |
| discount_pct | float | 0 to 100 |
| revision_count | integer | Greater than or equal to 0 |
| engagement_count | integer | Greater than or equal to 0 |

All four fields are required. Additional fields are rejected.

### Example Request

{
  "quote_value": 125000,
  "discount_pct": 10,
  "revision_count": 2,
  "engagement_count": 5
}

## 5. Prediction Response Contract

Successful response: HTTP 200

Response fields:

| Field | Type | Description |
|---|---|---|
| model_id | string | Model identifier |
| quote_value | float | Submitted quotation value |
| predicted_outcome | string | Won or Lost |
| win_probability | float | Predicted probability of Won |
| lost_probability | float | Predicted probability of Lost |
| data_status | string | Dataset classification |
| approval_status | string | Production approval status |

### Example Response

{
  "model_id": "DAY7_QUOTE_LOGISTIC",
  "quote_value": 125000,
  "predicted_outcome": "Lost",
  "win_probability": 0.462235,
  "lost_probability": 0.537765,
  "data_status": "Synthetic demonstration only",
  "approval_status": "Not approved for production use"
}

## 6. Validation Error Contract

Invalid requests return HTTP 422 Unprocessable Entity.

Validation scenarios tested:

- Zero quotation value
- Discount above 100%
- Negative revision count
- Negative engagement count
- Unexpected additional field
- Missing required field

## 7. Model Features

The prediction model uses:

1. Quote_Value
2. Discount_Pct
3. Revision_Count
4. Engagement_Count

The model is a StandardScaler and LogisticRegression pipeline.

## 8. Probability Interpretation

Win probability and lost probability represent model-estimated probabilities.

Their sum should be approximately 1.

These probabilities are exploratory outputs from a synthetic demonstration model and must not be treated as verified business outcomes.

## 9. API Documentation

Interactive Swagger documentation:

http://127.0.0.1:8000/docs

OpenAPI specification:

http://127.0.0.1:8000/openapi.json

## 10. Limitations

- Synthetic demonstration data only.
- Not approved for production use.
- Model probabilities are not validated business forecasts.
- No authentication or authorization implemented in this prototype.
- Local development deployment only.
