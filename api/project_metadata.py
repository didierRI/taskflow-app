"""TaskFlow API — project lifecycle metadata helpers."""

from __future__ import annotations

from datetime import datetime, timezone


def utc_timestamp() -> str:
    """Return the current UTC time in the API timestamp format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_project_record(
    project_id: str,
    name: str,
    *,
    workspace_id: str,
    timestamp: str,
) -> dict:
    """Build a project record with lifecycle metadata."""
    return {
        "id": project_id,
        "name": name,
        "workspace_id": workspace_id,
        "archived": False,
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def archive_project_record(project: dict, *, timestamp: str) -> dict:
    """Return an archived copy of a project record."""
    return {
        **project,
        "archived": True,
        "archived_at": timestamp,
        "updated_at": timestamp,
    }
