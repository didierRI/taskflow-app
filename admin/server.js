/**
 * TaskFlow Admin Service — Express server entry point.
 */

const express = require('express');
const usersRouter = require('./users');
const settingsRouter = require('./settings');

const app = express();
app.use(express.json());

app.use(usersRouter);
app.use(settingsRouter);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`TaskFlow admin service listening on port ${PORT}`);
});

module.exports = app;
