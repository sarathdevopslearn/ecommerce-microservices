
from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary in-memory product data.
# IDs match the Inventory Service.
products_data = {
    101: {
        "id": 101,
        "name": "Laptop",
        "price": 55000
    },
    102: {
        "id": 102,
        "name": "Wireless Mouse",
        "price": 800
    },
    103: {
        "id": 103,
        "name": "Keyboard",
        "price": 1500
    }
}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "service": "product-service",
        "status": "healthy"
    }), 200


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(list(products_data.values())), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = products_data.get(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product), 200


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    price = data.get("price")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "error": "A valid product name is required"
        }), 400

    if (
        isinstance(price, bool)
        or not isinstance(price, (int, float))
        or price <= 0
    ):
        return jsonify({
            "error": "Price must be a positive number"
        }), 400

    new_id = max(products_data.keys(), default=100) + 1

    product = {
        "id": new_id,
        "name": name.strip(),
        "price": price
    }

    products_data[new_id] = product

    return jsonify(product), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
