import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "User Service is running"


def test_create_user():
    client = app.test_client()

    response = client.post(
        "/users",
        json={
            "username": "sarath",
            "email": "sarath@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json["message"] == "User created successfully"
    assert response.json["user"]["username"] == "sarath"
    assert response.json["user"]["email"] == "sarath@example.com"


def test_create_user_missing_data():
    client = app.test_client()

    response = client.post(
        "/users",
        json={
            "username": "sarath",
        },
    )

    assert response.status_code == 400