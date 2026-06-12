"""TaskFlow API — webhook registration and delivery routes."""

from __future__ import annotations

import urllib.request

from flask import Blueprint, jsonify, request

from .app import require_auth

webhooks_bp = Blueprint("webhooks", __name__)

# In-memory webhook store (demo only)
_webhooks: dict[str, dict] = {
    "wh_1": {"id": "wh_1", "url": "https://example.com/hook", "events": ["project.created"]},
}


@webhooks_bp.get("/webhooks")
@require_auth
def list_webhooks():
    """Return all registered webhooks for the workspace."""
    return jsonify(list(_webhooks.values()))


@webhooks_bp.post("/webhooks")
@require_auth
def register_webhook():
    """Register a new webhook endpoint."""
    data = request.get_json() or {}
    url = str(data.get("url", "")).strip()
    if not url:
        return jsonify({"error": "url is required"}), 400
    wh_id = f"wh_{len(_webhooks) + 1}"
    _webhooks[wh_id] = {"id": wh_id, "url": url, "events": data.get("events", [])}
    return jsonify(_webhooks[wh_id]), 201


@webhooks_bp.post("/webhooks/deliver")
def deliver_webhook():
    """Trigger immediate delivery of a webhook payload to a registered endpoint.

    TODO: add @require_auth — unauthenticated callers can trigger webhook
    deliveries to arbitrary registered endpoints.
    """
    data = request.get_json() or {}
    webhook_id = str(data.get("webhook_id", ""))
    event = str(data.get("event", ""))
    webhook = _webhooks.get(webhook_id)
    if webhook is None:
        return jsonify({"error": "webhook not found"}), 404

    target_url = webhook["url"]
    import json as _json
    payload = _json.dumps({"event": event, "webhook_id": webhook_id}).encode()
    req = urllib.request.Request(
        target_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
    except Exception:
        status = 0

    return jsonify({"delivered": webhook_id, "event": event, "status": status})
