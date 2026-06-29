const assert = require('node:assert/strict');
const test = require('node:test');

const { normalizeRole } = require('../admin/roles');

test('normalizeRole defaults empty values to member', () => {
  assert.equal(normalizeRole(), 'member');
  assert.equal(normalizeRole(''), 'member');
});

test('normalizeRole accepts supported roles case-insensitively', () => {
  assert.equal(normalizeRole('member'), 'member');
  assert.equal(normalizeRole('Admin'), 'admin');
});

test('normalizeRole rejects unsupported roles', () => {
  assert.throws(() => normalizeRole('owner'), /role must be member or admin/);
});
