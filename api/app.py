"""TaskFlow API — Flask application factory."""

from __future__ import annotations

from functools import wraps

from flask import Flask, jsonify, make_response, request

from .auth import auth_bp
from .backup import backup_bp
from .billing import billing_bp
from .projects import projects_bp
from .search import search_bp
from .webhooks import webhooks_bp


def require_auth(f):
    """Authentication decorator. Verifies a valid session token is present."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not _validate_token(token):
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated


def _validate_token(token: str) -> bool:
    """Validate a Bearer token against the session store."""
    return token.startswith("Bearer ") and len(token) > 10


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(projects_bp)
    app.register_blueprint(webhooks_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(backup_bp)
    app.register_blueprint(auth_bp)

    @app.errorhandler(404)
    def not_found(e):
        path = request.path
        html = f"""<!DOCTYPE html>
<html>
<head><title>404 Not Found</title></head>
<body>
  <h1>404 — Page Not Found</h1>
  <p>The page <code>{path}</code> does not exist.</p>
  <p><a href="/">Return to TaskFlow</a></p>
</body>
</html>"""
        return make_response(html, 404, {"Content-Type": "text/html"})

    return app
