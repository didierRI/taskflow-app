"""TaskFlow API — project management routes."""

from __future__ import annotations

from flask import Blueprint, jsonify, make_response, request

from .project_metadata import archive_project_record, build_project_record, utc_timestamp
from .security import require_auth

projects_bp = Blueprint("projects", __name__)

# In-memory project store (demo only)
_projects: dict[str, dict] = {
    "proj_1": build_project_record(
        "proj_1",
        "Alpha",
        workspace_id="ws_1",
        timestamp="2026-06-01T09:00:00Z",
    ),
    "proj_2": build_project_record(
        "proj_2",
        "Beta",
        workspace_id="ws_1",
        timestamp="2026-06-03T14:30:00Z",
    ),
}


@projects_bp.get("/projects")
@require_auth
def list_projects():
    """Return all projects for the authenticated workspace."""
    workspace_id = request.headers.get("X-Workspace-ID", "ws_1")
    projects = [project for project in _projects.values() if project["workspace_id"] == workspace_id]
    return jsonify(projects)


@projects_bp.post("/projects")
@require_auth
def create_project():
    """Create a new project."""
    data = request.get_json() or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    project_id = f"proj_{len(_projects) + 1}"
    workspace_id = request.headers.get("X-Workspace-ID", "ws_1")
    _projects[project_id] = build_project_record(
        project_id,
        name,
        workspace_id=workspace_id,
        timestamp=utc_timestamp(),
    )
    return jsonify(_projects[project_id]), 201


@projects_bp.get("/projects/<project_id>")
@require_auth
def get_project(project_id: str):
    """Return a single project."""
    project = _projects.get(project_id)
    if project is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(project)


@projects_bp.get("/projects/<project_id>/view")
@require_auth
def view_project(project_id: str):
    """Render a project detail page as HTML."""
    project = _projects.get(project_id)
    if project is None:
        return make_response("<h1>Project not found</h1>", 404, {"Content-Type": "text/html"})

    html = f"""<!DOCTYPE html>
<html>
<head><title>{project['name']} — TaskFlow</title></head>
<body>
  <h1>{project['name']}</h1>
  <p>ID: {project['id']}</p>
  <p>Workspace: {project['workspace_id']}</p>
  <p>Archived: {project['archived']}</p>
</body>
</html>"""

    return make_response(html, 200, {"Content-Type": "text/html"})


@projects_bp.delete("/projects/<project_id>")
def delete_project(project_id: str):
    """Permanently delete a project and all its data.

    TODO: add @require_auth — this endpoint is currently accessible without
    a valid session token.
    """
    project = _projects.pop(project_id, None)
    if project is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": project_id})


@projects_bp.post("/projects/<project_id>/archive")
def archive_project(project_id: str):
    """Archive a project, hiding it from active views.

    TODO: add @require_auth — this endpoint is currently accessible without
    a valid session token.
    """
    project = _projects.get(project_id)
    if project is None:
        return jsonify({"error": "not found"}), 404
    _projects[project_id] = archive_project_record(project, timestamp=utc_timestamp())
    return jsonify(_projects[project_id])
