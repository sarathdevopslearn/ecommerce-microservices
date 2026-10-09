import pytest
from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["service"] == "Inventory Service"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_all_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.json) == 3


def test_get_existing_product_inventory(client):
    response = client.get("/inventory/101")
    assert response.status_code == 200
    assert response.json["quantity"] == 50


def test_get_missing_product_inventory(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    assert response.json["error"] == "Product not found"