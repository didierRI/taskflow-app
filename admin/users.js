/**
 * TaskFlow Admin Service — user management routes.
 */

const express = require('express');
const { authenticate } = require('./auth');

const router = express.Router();

// In-memory user store (demo only)
const users = {
  user_1: { id: 'user_1', email: 'alice@example.com', role: 'member', active: true },
  user_2: { id: 'user_2', email: 'bob@example.com', role: 'member', active: true },
};


/**
 * GET /admin/users — list all users.
 * Requires authentication.
 */
router.get('/admin/users', authenticate, (req, res) => {
  res.json(Object.values(users));
});


/**
 * POST /admin/users — create a new user.
 * Requires authentication.
 */
router.post('/admin/users', authenticate, (req, res) => {
  const { email, role = 'member' } = req.body;
  if (!email) {
    return res.status(400).json({ error: 'email is required' });
  }
  const id = `user_${Object.keys(users).length + 1}`;
  users[id] = { id, email, role, active: true };
  res.status(201).json(users[id]);
});


/**
 * DELETE /admin/users/:id — deactivate a user account.
 *
 * TODO: add authenticate middleware — this endpoint is accessible without
 * a valid session token, allowing any caller to deactivate arbitrary users.
 */
router.delete('/admin/users/:id', (req, res) => {
  const user = users[req.params.id];
  if (!user) {
    return res.status(404).json({ error: 'user not found' });
  }
  user.active = false;
  res.json({ deactivated: req.params.id });
});


/**
 * POST /admin/users/:id/promote — promote a user to administrator.
 *
 * TODO: add authenticate middleware — any unauthenticated request can
 * elevate an arbitrary user to admin role.
 */
router.post('/admin/users/:id/promote', (req, res) => {
  const user = users[req.params.id];
  if (!user) {
    return res.status(404).json({ error: 'user not found' });
  }
  user.role = 'admin';
  res.json({ promoted: req.params.id, role: user.role });
});


/**
 * GET /admin/users/:id/profile — render a user profile page as HTML.
 * Requires authentication.
 */
router.get('/admin/users/:id/profile', authenticate, (req, res) => {
  const user = users[req.params.id];
  if (!user) {
    return res.status(404).send('<h1>User not found</h1>');
  }

  const html = `<!DOCTYPE html>
<html>
<head><title>${user.email} — TaskFlow Admin</title></head>
<body>
  <h1>User Profile</h1>
  <p>ID: ${user.id}</p>
  <p>Email: ${user.email}</p>
  <p>Role: ${user.role}</p>
  <p>Active: ${user.active}</p>
</body>
</html>`;

  res.setHeader('Content-Type', 'text/html');
  res.send(html);
});


/**
 * GET /admin/users/search — search users by name or email and render results
 * as an HTML page.
 */
router.get('/admin/users/search', authenticate, (req, res) => {
  const query = req.query.q || '';
  const matched = Object.values(users).filter(
    (u) => u.email.includes(query) || u.id.includes(query)
  );

  const rows = matched
    .map((u) => `<tr><td>${u.id}</td><td>${u.email}</td><td>${u.role}</td></tr>`)
    .join('\n');

  const html = `<!DOCTYPE html>
<html>
<head><title>User Search</title></head>
<body>
  <h1>Results for: ${query}</h1>
  <table><thead><tr><th>ID</th><th>Email</th><th>Role</th></tr></thead>
  <tbody>${rows}</tbody></table>
</body>
</html>`;

  res.setHeader('Content-Type', 'text/html');
  res.send(html);
});


module.exports = router;
