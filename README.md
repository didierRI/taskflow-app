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
