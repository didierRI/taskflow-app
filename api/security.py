"""TaskFlow API — shared request security helpers."""

from __future__ import annotations

from functools import wraps
from typing import Callable


def validate_bearer_token(token: str | None) -> bool:
    """Return True when a request token uses the expected bearer format."""
    return bool(token and token.startswith("Bearer ") and len(token) > 12)


def require_auth(f: Callable):
    """Authentication decorator. Verifies a valid session token is present."""

    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import jsonify, request

        token = request.headers.get("Authorization")
        if not validate_bearer_token(token):
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)

    return decorated
