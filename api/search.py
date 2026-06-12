"""TaskFlow API — project search routes."""

from __future__ import annotations

from flask import Blueprint, make_response, request

search_bp = Blueprint("search", __name__)


@search_bp.get("/search/results")
def search_results():
    """Return an HTML search-results page for the given query."""
    query = request.args.get("q", "")

    html = f"""<!DOCTYPE html>
<html>
<head><title>TaskFlow Search</title></head>
<body>
  <h1>Search Results</h1>
  <p>Showing results for: {query}</p>
  <ul id="results"></ul>
</body>
</html>"""

    return make_response(html, 200, {"Content-Type": "text/html"})
