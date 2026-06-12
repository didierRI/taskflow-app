/**
 * TaskFlow Admin Service — Express server entry point.
 */

const express = require('express');
const usersRouter = require('./users');
const settingsRouter = require('./settings');

const app = express();
app.use(express.json());

/**
 * Authentication middleware. Validates the Authorization header.
 * Must be applied per-router or per-route.
 */
function authenticate(req, res, next) {
  const token = req.headers['authorization'];
  if (!token || !token.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  // Token validation against session store would go here.
  next();
}

// Export authenticate so routers can use it selectively.
module.exports.authenticate = authenticate;

app.use(usersRouter);
app.use(settingsRouter);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`TaskFlow admin service listening on port ${PORT}`);
});

module.exports = app;
