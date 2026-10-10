from flask import Flask, jsonify, request
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from uuid import uuid4

app = Flask(__name__)

payments = {}
next_id = 1


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "payment-service"
    }), 200


@app.route("/payments", methods=["POST"])
def create_payment():
    global next_id

    data = request.get_json(silent=True) or {}

    required_fields = ["order_id", "user_id", "amount", "payment_method"]

    if not all(data.get(field) is not None for field in required_fields):
        return jsonify({
            "error": "order_id, user_id, amount and payment_method are required"
        }), 400

    try:
        amount = Decimal(str(data["amount"]))
    except (InvalidOperation, ValueError):
        return jsonify({"error": "amount must be a valid number"}), 400

    if not amount.is_finite() or amount <= 0:
        return jsonify({"error": "amount must be greater than zero"}), 400

    if amount.as_tuple().exponent < -2:
        return jsonify({"error": "amount cannot have more than 2 decimal places"}), 400

    payment_method = data["payment_method"]

    if not isinstance(payment_method, str) or payment_method not in [
        "card", "upi", "net_banking", "wallet"
    ]:
        return jsonify({
            "error": "payment_method must be card, upi, net_banking or wallet"
        }), 400

    payment = {
        "id": next_id,
        "transaction_id": str(uuid4()),
        "order_id": data["order_id"],
        "user_id": data["user_id"],
        "amount": str(amount),
        "currency": data.get("currency", "INR"),
        "payment_method": payment_method,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    payments[next_id] = payment
    next_id += 1

    return jsonify(payment), 201


@app.route("/payments", methods=["GET"])
def get_payments():
    order_id = request.args.get("order_id")
    user_id = request.args.get("user_id")

    result = list(payments.values())

    if order_id is not None:
        result = [
            payment for payment in result
            if str(payment["order_id"]) == order_id
        ]

    if user_id is not None:
        result = [
            payment for payment in result
            if str(payment["user_id"]) == user_id
        ]

    return jsonify(result), 200


@app.route("/payments/<int:payment_id>", methods=["GET"])
def get_payment(payment_id):
    payment = payments.get(payment_id)

    if payment is None:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify(payment), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
