"""TaskFlow API — workspace backup and restore routes."""

from __future__ import annotations

import base64
import pickle

from flask import Blueprint, jsonify, request

from .app import require_auth

backup_bp = Blueprint("backup", __name__)


@backup_bp.get("/backup/export")
@require_auth
def export_workspace():
    """Export the current workspace state as a base64-encoded snapshot."""
    data = {"workspaceId": "ws_1", "plan": "pro", "exportedAt": "2026-05-21"}
    payload = base64.b64encode(pickle.dumps(data)).decode()
    return jsonify({"snapshot": payload})


@backup_bp.post("/backup/restore")
@require_auth
def restore_workspace():
    """Restore workspace state from a previously exported snapshot."""
    body = request.get_json() or {}
    snapshot = body.get("snapshot", "")
    if not snapshot:
        return jsonify({"error": "snapshot is required"}), 400

    data = pickle.loads(base64.b64decode(snapshot))

    return jsonify({"restored": True, "workspace": data.get("workspaceId")})
