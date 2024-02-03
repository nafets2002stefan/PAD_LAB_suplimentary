const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const db = mongoose.connection;

// status route endpoint
router.get('/status', (req, res) => {
  const dbStatus = db.readyState === 1 ? 'Connected' : 'Disconnected';

  const status = {
      service: 'Content Management and Analytics Service',
      status: 'OK',
      database: dbStatus
  };

  res.json(status);
});

module.exports = router;
