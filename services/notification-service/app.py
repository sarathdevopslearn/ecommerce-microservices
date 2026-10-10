from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

notifications = []
next_id = 1


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "notification-service"
    }), 200


@app.route("/notifications", methods=["POST"])
def create_notification():
    global next_id

    data = request.get_json(silent=True) or {}

    required_fields = ["user_id", "message", "type"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({
            "error": "user_id, message and type are required"
        }), 400

    notification = {
        "id": next_id,
        "user_id": data["user_id"],
        "message": data["message"],
        "type": data["type"],
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    notifications.append(notification)
    next_id += 1

    return jsonify(notification), 201


@app.route("/notifications", methods=["GET"])
def get_notifications():
    user_id = request.args.get("user_id")

    if user_id:
        result = [
            item for item in notifications
            if str(item["user_id"]) == user_id
        ]
    else:
        result = notifications

    return jsonify(result), 200


@app.route("/notifications/<int:notification_id>", methods=["GET"])
def get_notification(notification_id):
    for notification in notifications:
        if notification["id"] == notification_id:
            return jsonify(notification), 200

    return jsonify({"error": "Notification not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
