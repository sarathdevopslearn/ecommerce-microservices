from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "order-service",
    }


def test_create_order():
    response = client.post(
        "/orders",
        json={
            "user_id": 1,
            "product_id": 101,
            "quantity": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["order_id"] >= 1
    assert data["user_id"] == 1
    assert data["product_id"] == 101
    assert data["quantity"] == 2
    assert data["status"] == "created"


def test_invalid_quantity():
    response = client.post(
        "/orders",
        json={
            "user_id": 1,
            "product_id": 101,
            "quantity": 0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Quantity must be greater than 0"