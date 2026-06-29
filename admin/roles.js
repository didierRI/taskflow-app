/**
 * TaskFlow Admin Service — user role helpers.
 */

const SUPPORTED_ROLES = new Set(['member', 'admin']);

function normalizeRole(role = 'member') {
  const normalized = String(role || 'member').trim().toLowerCase();
  if (!SUPPORTED_ROLES.has(normalized)) {
    throw new Error('role must be member or admin');
  }
  return normalized;
}

module.exports = { normalizeRole };
