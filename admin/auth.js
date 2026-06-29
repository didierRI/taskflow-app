/**
 * TaskFlow Admin Service — shared authentication middleware.
 */

function hasBearerToken(headers = {}) {
  const token = headers.authorization || headers.Authorization;
  return Boolean(token && token.startsWith('Bearer ') && token.length > 'Bearer '.length);
}

function authenticate(req, res, next) {
  if (!hasBearerToken(req.headers)) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  // Token validation against session store would go here.
  next();
}

module.exports = { authenticate, hasBearerToken };
