import httpx
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def mock_httpx_get(url, **kwargs):
    request = httpx.Request("GET", url)

    if "/users/" in url:
        return httpx.Response(
            200,
            json={
                "username": "testuser",
                "message": "User retrieved successfully",
            },
            request=request,
        )

    if "/products/101" in url:
        return httpx.Response(
            200,
            json={
                "id": 101,
                "name": "Laptop",
                "price": 55000,
            },
            request=request,
        )

    if "/inventory/101" in url:
        return httpx.Response(
            200,
            json={
                "product_id": 101,
                "quantity": 50,
            },
            request=request,
        )

    return httpx.Response(404, json={"error": "Not found"}, request=request)


def mock_httpx_post(url, **kwargs):
    request = httpx.Request("POST", url)

    if "/payments" in url:
        return httpx.Response(
            201,
            json={
                "id": 1,
                "order_id": 1,
                "user_id": 1,
                "amount": 110000,
                "status": "pending",
            },
            request=request,
        )

    if "/notifications" in url:
        return httpx.Response(
            201,
            json={
                "id": 1,
                "user_id": 1,
                "message": "Order created",
                "type": "order_created",
                "status": "pending",
            },
            request=request,
        )

    return httpx.Response(404, json={"error": "Not found"}, request=request)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "order-service",
    }


def test_create_order(monkeypatch):
    monkeypatch.setattr(httpx, "get", mock_httpx_get)
    monkeypatch.setattr(httpx, "post", mock_httpx_post)

    response = client.post(
        "/orders",
        json={
            "user_id": 1,
            "username": "testuser",
            "product_id": 101,
            "quantity": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 1
    assert data["product_id"] == 101
    assert data["quantity"] == 2
    assert data["total_amount"] == 110000
    assert data["status"] == "created"
    assert data["payment"]["status"] == "pending"
    assert data["notification"]["type"] == "order_created"


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
