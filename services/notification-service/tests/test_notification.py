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
    assert response.json["service"] == "notification-service"


def test_create_notification(client):
    response = client.post(
        "/notifications",
        json={
            "user_id": 101,
            "message": "Your order has been confirmed",
            "type": "order_confirmation"
        }
    )

    assert response.status_code == 201
    assert response.json["user_id"] == 101
    assert response.json["status"] == "pending"


def test_create_notification_missing_fields(client):
    response = client.post(
        "/notifications",
        json={"user_id": 101}
    )

    assert response.status_code == 400


def test_get_notifications(client):
    client.post(
        "/notifications",
        json={
            "user_id": 202,
            "message": "Your order has shipped",
            "type": "shipping_update"
        }
    )

    response = client.get("/notifications?user_id=202")

    assert response.status_code == 200
    assert len(response.json) >= 1
    assert response.json[-1]["user_id"] == 202


def test_notification_not_found(client):
    response = client.get("/notifications/999999")

    assert response.status_code == 404
