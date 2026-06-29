# TaskFlow

A project management SaaS API. This repository contains two services:

- **`api/`** — Python Flask REST API (projects, webhooks, billing)
- **`admin/`** — Node.js Express admin service (user management, org settings)

## Services

### API service (`api/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/projects` | GET, POST | List and create projects |
| `/projects/<id>` | GET, DELETE | Get or delete a project |
| `/projects/<id>/archive` | POST | Archive a project |
| `/webhooks` | GET, POST | List and register webhooks |
| `/webhooks/deliver` | POST | Trigger webhook delivery |
| `/billing/status` | GET | Get billing status |
| `/billing/cancel` | POST | Cancel a subscription |

### Admin service (`admin/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/users` | GET, POST | List and create users |
| `/admin/users/:id` | DELETE | Deactivate a user |
| `/admin/users/:id/promote` | POST | Promote a user to admin |
| `/admin/settings` | GET, PUT | Get and update org settings |
| `/admin/settings/reset` | POST | Reset org settings to defaults |

## Local development

### API service

Run the Flask API from the repository root:

```bash
flask --app api.app:create_app run --debug --port 5000
```

Authenticated API routes expect a bearer token. Workspace-scoped routes also
accept an `X-Workspace-ID` header:

```bash
curl http://localhost:5000/projects \
  -H "Authorization: Bearer demo-token" \
  -H "X-Workspace-ID: ws_1"
```

Create a project:

```bash
curl http://localhost:5000/projects \
  -X POST \
  -H "Authorization: Bearer demo-token" \
  -H "X-Workspace-ID: ws_1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Launch Plan"}'
```

Check billing status:

```bash
curl http://localhost:5000/billing/status \
  -H "Authorization: Bearer demo-token" \
  -H "X-Workspace-ID: ws_1"
```

### Admin service

Run the admin service from `admin/`:

```bash
node server.js
```

Admin routes use the same bearer-token convention:

```bash
curl http://localhost:3001/admin/users \
  -H "Authorization: Bearer demo-token"
```

Create a user:

```bash
curl http://localhost:3001/admin/users \
  -X POST \
  -H "Authorization: Bearer demo-token" \
  -H "Content-Type: application/json" \
  -d '{"email":"casey@example.com","role":"member"}'
```

## Demo notes

TaskFlow uses in-memory stores so data resets when either service restarts. The
sample records are intentionally small and are meant to make endpoint behavior
easy to inspect during demos.
