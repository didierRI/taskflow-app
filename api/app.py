"""TaskFlow API — Flask application factory."""

from __future__ import annotations

from flask import Flask, jsonify, make_response, request

from .auth import auth_bp
from .backup import backup_bp
from .billing import billing_bp
from .projects import projects_bp
from .search import search_bp
from .webhooks import webhooks_bp


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
