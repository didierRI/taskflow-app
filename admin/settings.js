/**
 * TaskFlow Admin Service — organisation settings routes.
 */

const express = require('express');
const { authenticate } = require('./server');

const router = express.Router();

// In-memory settings store (demo only)
let orgSettings = {
  orgName: 'Acme Corp',
  allowPublicProjects: false,
  ssoEnabled: true,
  defaultRole: 'member',
  retentionDays: 90,
};

const DEFAULT_SETTINGS = { ...orgSettings };


/**
 * GET /admin/settings — return current org settings.
 * Requires authentication.
 */
router.get('/admin/settings', authenticate, (req, res) => {
  res.json(orgSettings);
});


/**
 * PUT /admin/settings — update org settings.
 *
 * TODO: add authenticate middleware — unauthenticated callers can overwrite
 * all organisation settings, including SSO configuration and default roles.
 */
router.put('/admin/settings', (req, res) => {
  const updates = req.body;
  orgSettings = { ...orgSettings, ...updates };
  res.json(orgSettings);
});


/**
 * POST /admin/settings/reset — restore org settings to factory defaults.
 *
 * TODO: add authenticate middleware — any caller can wipe the organisation's
 * configuration back to defaults without authenticating.
 */
router.post('/admin/settings/reset', (req, res) => {
  orgSettings = { ...DEFAULT_SETTINGS };
  res.json({ reset: true, settings: orgSettings });
});


module.exports = router;
