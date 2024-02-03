var express = require('express');
const router = express.Router();
const axios = require('axios');
const Sport = require('../models/sportModel');

// handling logging when a user views a piece of content
router.post('/sports', async (req, res) => {
  const { sportName } = req.body;

  const options = {
    method: 'GET',
    url: `https://bet365-api-inplay.p.rapidapi.com/bet365/get_sport_events/${sportName}`,
    headers: {
      'X-RapidAPI-Key': 'ca38fc6972msh71c5fff2c07a60ap129cd0jsn90d943df6445',
      'X-RapidAPI-Host': 'bet365-api-inplay.p.rapidapi.com'
    }
  };

  const APIResponse = await axios.request(options);
  const sportData = APIResponse.data[0];
  const mappedData = {
    registrationId: sportData.eventId,
    sportName: sportData.sport,
    team1: sportData.team1,
    team2: sportData.team2,
    score: sportData.score,
    liga: sportData.liga,
    timestamp: Date.now()
  };
  try {

    console.log(mappedData);
  } catch (error) {
    console.error(error);
  }

  try {
    const sport = new Sport({
      registrationId: mappedData.registrationId,
      sportName : mappedData.sportName,
      team1: mappedData.team1,
      team2: mappedData.team2,
      score: mappedData.score,
      liga: mappedData.liga,
      timestamp: mappedData.timestamp
    });
    console.log("sportdaa");
    await sport.save();
    return res.json({ message: 'View sport logged successfully' });
  } catch (error) {
    console.log(error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/sports', async (req, res) => {
    try {
      const sports = await Sport.find();
      res.status(200).json(sports);
    } catch (error) {
      res.status(404).json({message: error.message});
    }
});

router.get('/sports/:registrationId', async (req, res) => {
  const { registrationId } = req.params;
  try {
    const sports = await Sport.find({ registrationId });

    const uniqueSportIds = [...new Set(sports.map(sport => sport.registrationId))];
    res.json({ contentIds : sports});
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.delete('/sports/:registrationId', async (req, res) => {
  const { registrationId } = req.params;
  try {
    // Find and delete sports with the given registration ID
    const result = await Sport.deleteMany({ registrationId });

    if (result.deletedCount > 0) {
      res.json({ message: 'Sports deleted successfully' });
    } else {
      res.status(404).json({ error: 'No matching sports found for the given registration ID' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


module.exports = router;

