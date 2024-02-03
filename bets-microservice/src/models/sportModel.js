const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const sportSchema = new Schema({
  registrationId: {
    type: String,
    required: true
  },
  sportName: {
    type: String,
    required: true
  },
  team1: {
    type: String,
    required: true
  },
  team2: {
    type: String,
    required: true
  },
  score: {
    type: String,
    required: true
  },
  liga: {
    type: String,
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  },
});

sportSchema.index(
    { registrationId: 1, sportName: 1, team1: 1, team2:1, score: 1, liga: 1}, 
    { unique: true }
  );

const Sport = mongoose.model('Sport', sportSchema);

module.exports = Sport;