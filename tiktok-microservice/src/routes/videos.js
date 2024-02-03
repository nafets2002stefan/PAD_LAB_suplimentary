var express = require('express');
const axios = require('axios');
const Video = require('../model/videoModel');
const router = express.Router();


//CRUD operations for content
router.post('/videos', async (req, res) => {

    const { videoName } = req.body;
    const options = {
        method: 'GET',
        url: 'https://tiktok-all-in-one.p.rapidapi.com/search/video',
        params: {
          query: `${videoName}`,
          offset: '20',
          sort: '1',
          time: '7'
        },
        headers: {
          'X-RapidAPI-Key': 'ca38fc6972msh71c5fff2c07a60ap129cd0jsn90d943df6445',
          'X-RapidAPI-Host': 'tiktok-all-in-one.p.rapidapi.com'
        }
      };
      
      const APIResponse = await axios.request(options);
      const videoData = APIResponse.data;
      console.log(videoData);
      const mappedData = {
          videoId: videoData.extra.logid,
          description: videoData.extra.dc,
          music: videoData.global_doodle_config.search_channel,
      };
      console.log(mappedData);

      try {
          const video = new Video({
              videoId : mappedData.videoId,
              description: mappedData.description,
              music: mappedData.music,
          });
          
          console.log(video, "testing");
        await video.save();
        return res.status(201).json({ message: 'Content added succesfully.' });
    } catch (error) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

router.get('/videos', async (req, res) => {
    try {
        const videos = await Video.find();
        res.status(200).json(videos);
    } catch (error) {
        res.status(404).json({message: error.message});
    }
})

router.get('/videos/:videoId', async (req, res) => {
    const videoId = req.params;
    // console.log(`Video ID: ${videoId}`);

    try {
        const video = await Video.findOne(videoId);

        if (!video) {
            return res.status(404).json({ error: 'Video not found' });
        }

        return res.status(200).json(video);
    } catch (error) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

router.delete('/videos/:videoId', async (req, res) => {
    const videoId = req.params.videoId;
    // console.log(`Video ID: ${videoId}`);

    try {
        const video = await Video.findOne({videoId});

        if (!video) {
            return res.status(404).json({ error: 'Video not found' });
        }

        await video.deleteOne();

        return res.status(200).json({ message: 'Video deleted successfully.' });
    } catch (error) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});


module.exports = router;