from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "service": "product-service",
        "status": "healthy"
    })


@app.route("/products", methods=["GET"])
def products():
    return jsonify([
        {
            "id": 1,
            "name": "Laptop",
            "price": 55000
        },
        {
            "id": 2,
            "name": "Wireless Mouse",
            "price": 800
        }
    ])


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    product = {
        "id": 3,
        "name": data["name"],
        "price": data["price"]
    }

    return jsonify(product), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)