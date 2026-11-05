import pytest

from app.main import create_app

CATALOG = [
    {"sku": "A-1", "name": "Item A", "category": "x", "price": 1.0, "stock": 3},
    {"sku": "B-2", "name": "Item B", "category": "x", "price": 2.0, "stock": 4},
    {"sku": "C-3", "name": "Item C", "category": "y", "price": 3.0, "stock": 5},
]


@pytest.fixture
def client():
    return create_app(CATALOG).test_client()


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_filter_by_category(client):
    skus = [p["sku"] for p in client.get("/products?category=x").get_json()]
    assert skus == ["A-1", "B-2"]


def test_unknown_product_returns_404(client):
    assert client.get("/products/NOPE").status_code == 404


def test_stock_summary(client):
    assert client.get("/stock/summary").get_json() == {
        "x": {"products": 2, "units": 7},
        "y": {"products": 1, "units": 5},
    }


def test_default_catalog_loads():
    response = create_app().test_client().get("/products/KB-001")
    assert response.get_json()["name"] == "Mechanical keyboard"
