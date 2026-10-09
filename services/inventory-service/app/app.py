from flask import Flask, jsonify

app = Flask(__name__)

# Temporary in-memory inventory data
inventory = {
    101: {"product_id": 101, "quantity": 50},
    102: {"product_id": 102, "quantity": 30},
    103: {"product_id": 103, "quantity": 20},
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Inventory Service",
        "status": "running"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(list(inventory.values())), 200


@app.route("/inventory/<int:product_id>", methods=["GET"])
def get_product_inventory(product_id):
    item = inventory.get(product_id)

    if item is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(item), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)