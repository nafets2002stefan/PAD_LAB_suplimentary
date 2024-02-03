const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const videoSchema = new Schema({
  videoId: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: false
  },
  music: {
    type: String,
    required: false
  }
});

videoSchema.index(
    { videoId: 1, description: 1, music:1}, 
    { unique: true }
  );

const Video = mongoose.model('Video', videoSchema);

module.exports = Video;