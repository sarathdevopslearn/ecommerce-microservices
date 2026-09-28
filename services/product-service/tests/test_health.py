from app.main import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["service"] == "product-service"
    assert data["status"] == "healthy"


def test_create_product():
    client = app.test_client()

    response = client.post(
        "/products",
        json={
            "name": "Keyboard",
            "price": 1500
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 3
    assert data["name"] == "Keyboard"
    assert data["price"] == 1500