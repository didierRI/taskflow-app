const assert = require('node:assert/strict');
const test = require('node:test');

const { hasBearerToken } = require('../admin/auth');

test('hasBearerToken rejects missing and malformed headers', () => {
  assert.equal(hasBearerToken({}), false);
  assert.equal(hasBearerToken({ authorization: 'token' }), false);
  assert.equal(hasBearerToken({ authorization: 'Bearer ' }), false);
});

test('hasBearerToken accepts bearer authorization headers', () => {
  assert.equal(hasBearerToken({ authorization: 'Bearer demo-token' }), true);
});
