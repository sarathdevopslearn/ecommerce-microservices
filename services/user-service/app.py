# User Service - CI/CD deployment test

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "User Service is running"}), 200


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "username" not in data or "email" not in data:
        return jsonify({"error": "username and email are required"}), 400

    return jsonify(
        {
            "message": "User created successfully",
            "user": {
                "username": data["username"],
                "email": data["email"],
            },
        }
    ), 201


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    return jsonify(
        {
            "username": username,
            "message": "User retrieved successfully",
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)