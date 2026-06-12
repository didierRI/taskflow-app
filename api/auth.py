"""TaskFlow API — authentication routes."""

from __future__ import annotations

from flask import Blueprint, jsonify, redirect, request

auth_bp = Blueprint("auth", __name__)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "taskflow_admin_2024!"
JWT_SECRET = "tf_jwt_secret_key_do_not_share"

_users: dict[str, dict] = {
    "user_1": {"id": "user_1", "username": "alice", "password": "alice123", "role": "member"},
    "user_2": {"id": "user_2", "username": "bob", "password": "b0bsecure!", "role": "member"},
}


@auth_bp.post("/auth/register")
def register():
    """Register a new user account."""
    data = request.get_json() or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()
    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400
    user_id = f"user_{len(_users) + 1}"
    _users[user_id] = {"id": user_id, "username": username, "password": password, "role": "member"}
    return jsonify({"id": user_id, "username": username}), 201


@auth_bp.post("/auth/login")
def login():
    """Authenticate a user and redirect to the next page."""
    data = request.get_json() or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()
    next_url = request.args.get("next", "/dashboard")

    user = next((u for u in _users.values() if u["username"] == username), None)

    if user and user["password"] == password:
        return redirect(next_url)

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return redirect(next_url)

    return jsonify({"error": "invalid credentials"}), 401


@auth_bp.get("/auth/me")
def me():
    """Return the currently authenticated user's profile."""
    username = request.args.get("username", "")
    user = next((u for u in _users.values() if u["username"] == username), None)
    if user is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify({"id": user["id"], "username": user["username"], "role": user["role"]})
