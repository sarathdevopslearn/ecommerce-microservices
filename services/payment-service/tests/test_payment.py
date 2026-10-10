import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["service"] == "payment-service"


def test_create_payment(client):
    response = client.post(
        "/payments",
        json={
            "order_id": 101,
            "user_id": 201,
            "amount": 1499.99,
            "payment_method": "upi"
        }
    )

    assert response.status_code == 201
    assert response.json["order_id"] == 101
    assert response.json["user_id"] == 201
    assert response.json["status"] == "pending"
    assert response.json["currency"] == "INR"
    assert "transaction_id" in response.json


def test_create_payment_missing_fields(client):
    response = client.post(
        "/payments",
        json={"order_id": 101}
    )

    assert response.status_code == 400


def test_create_payment_invalid_amount(client):
    response = client.post(
        "/payments",
        json={
            "order_id": 102,
            "user_id": 202,
            "amount": -100,
            "payment_method": "upi"
        }
    )

    assert response.status_code == 400


def test_create_payment_invalid_method(client):
    response = client.post(
        "/payments",
        json={
            "order_id": 103,
            "user_id": 203,
            "amount": 500,
            "payment_method": "cash"
        }
    )

    assert response.status_code == 400


def test_get_payments(client):
    client.post(
        "/payments",
        json={
            "order_id": 104,
            "user_id": 204,
            "amount": 250,
            "payment_method": "card"
        }
    )

    response = client.get("/payments?order_id=104")

    assert response.status_code == 200
    assert len(response.json) >= 1
    assert str(response.json[-1]["order_id"]) == "104"


def test_payment_not_found(client):
    response = client.get("/payments/999999")

    assert response.status_code == 404
