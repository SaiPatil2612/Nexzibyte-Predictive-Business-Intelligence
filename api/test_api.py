
import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

VALID_REQUEST = {
    "quote_value": 125000,
    "discount_pct": 10,
    "revision_count": 2,
    "engagement_count": 5,
}


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True


def test_valid_quotation_prediction():
    response = client.post(
        "/api/v1/predict/quotation",
        json=VALID_REQUEST,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["model_id"] == "DAY7_QUOTE_LOGISTIC"
    assert data["predicted_outcome"] in ["Won", "Lost"]
    assert 0 <= data["win_probability"] <= 1
    assert 0 <= data["lost_probability"] <= 1
    assert abs(
        data["win_probability"] + data["lost_probability"] - 1
    ) < 0.00001
    assert data["data_status"] == "Synthetic demonstration only"
    assert data["approval_status"] == "Not approved for production use"


def test_boundary_values():
    request_data = {
        "quote_value": 1,
        "discount_pct": 100,
        "revision_count": 0,
        "engagement_count": 0,
    }

    response = client.post(
        "/api/v1/predict/quotation",
        json=request_data,
    )

    assert response.status_code == 200


def test_zero_quote_value_rejected():
    data = {**VALID_REQUEST, "quote_value": 0}

    response = client.post("/api/v1/predict/quotation", json=data)

    assert response.status_code == 422


def test_discount_above_100_rejected():
    data = {**VALID_REQUEST, "discount_pct": 101}

    response = client.post("/api/v1/predict/quotation", json=data)

    assert response.status_code == 422


def test_negative_revision_count_rejected():
    data = {**VALID_REQUEST, "revision_count": -1}

    response = client.post("/api/v1/predict/quotation", json=data)

    assert response.status_code == 422


def test_negative_engagement_count_rejected():
    data = {**VALID_REQUEST, "engagement_count": -1}

    response = client.post("/api/v1/predict/quotation", json=data)

    assert response.status_code == 422


def test_extra_field_rejected():
    data = {
        **VALID_REQUEST,
        "customer_name": "Test Customer",
    }

    response = client.post("/api/v1/predict/quotation", json=data)

    assert response.status_code == 422


def test_missing_engagement_count_rejected():
    data = {
        "quote_value": 125000,
        "discount_pct": 10,
        "revision_count": 2,
    }

    response = client.post("/api/v1/predict/quotation", json=data)

    assert response.status_code == 422
