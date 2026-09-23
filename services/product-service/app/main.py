from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "product-service"
    })


@app.route("/products")
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)