"""TaskFlow API — billing and subscription routes."""

from __future__ import annotations

from flask import Blueprint, jsonify, make_response, request

from .app import require_auth

billing_bp = Blueprint("billing", __name__)

# In-memory subscription store (demo only)
_subscriptions: dict[str, dict] = {
    "sub_1": {"id": "sub_1", "plan": "pro", "status": "active", "workspace_id": "ws_1"},
}


@billing_bp.get("/billing/status")
@require_auth
def billing_status():
    """Return the current subscription status for the authenticated workspace."""
    workspace_id = request.headers.get("X-Workspace-ID", "ws_1")
    for sub in _subscriptions.values():
        if sub["workspace_id"] == workspace_id:
            return jsonify(sub)
    return jsonify({"status": "no_subscription"})


@billing_bp.get("/billing/portal")
@require_auth
def billing_portal():
    """Render the billing portal page for the current workspace."""
    workspace_id = request.headers.get("X-Workspace-ID", "ws_1")
    plan_name = request.args.get("plan", "free")

    sub = next(
        (s for s in _subscriptions.values() if s["workspace_id"] == workspace_id),
        None,
    )
    status = sub["status"] if sub else "no_subscription"

    html = f"""<!DOCTYPE html>
<html>
<head><title>TaskFlow Billing Portal</title></head>
<body>
  <h1>Billing Portal</h1>
  <p>Workspace: {workspace_id}</p>
  <p>Current plan: {plan_name}</p>
  <p>Status: {status}</p>
</body>
</html>"""

    return make_response(html, 200, {"Content-Type": "text/html"})


@billing_bp.post("/billing/cancel")
def cancel_subscription():
    """Cancel an active subscription immediately.

    TODO: add @require_auth — any caller can cancel any subscription by ID
    without authenticating.
    """
    data = request.get_json() or {}
    subscription_id = str(data.get("subscription_id", ""))
    sub = _subscriptions.get(subscription_id)
    if sub is None:
        return jsonify({"error": "subscription not found"}), 404
    sub["status"] = "cancelled"
    return jsonify({"cancelled": subscription_id})
