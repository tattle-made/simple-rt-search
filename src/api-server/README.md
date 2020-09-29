# API Server

an always on rabbit mq consumer that generates hashes of images and videos and stores them in an elastic search

v 0.0.3

```
cd src/api-server
docker build -t simple-rt-search-api .
docker run -v $(pwd):/app --name simple-rt-search-api -p 5000:5000 simple-rt-search-api
```

Test Commands

```
curl -H "Content-Type: application/json" -X POST -v --data '{"file_url":"https://tattle-media.s3.amazonaws.com/test-data/videos/cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4","media_type":"video","bucket_name":"tattle-media", "file_name":"cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4", "filepath_prefix":"test-data/videos/" ,"metadata":{"source":"khoj","source_id":23423423432}}' http://localhost:5000/media

curl -H "Content-Type: application/json" -X POST -v --data '{"file_url":"https://tattle-media.s3.amazonaws.com/test-data/audios/audio_1.mp3","media_type":"audio","bucket_name":"tattle-media", "file_name":"audio_1.mp3", "filepath_prefix":"test-data/audios/" ,"metadata":{"source":"khoj","source_id":23423423432}}' http://localhost:5000/media

curl -H "Content-Type: application/json" -X POST -v --data '{"file_url":"https://tattle-media.s3.amazonaws.com/test-data/images/004e0126-2ef6-41de-97be-e0b9daaee480.jpeg","media_type":"image","bucket_name":"tattle-media", "file_name":"004e0126-2ef6-41de-97be-e0b9daaee480.jpeg", "filepath_prefix":"test-data/images/" ,"metadata":{"source":"khoj","source_id":23423423432}}' http://localhost:5000/media



```

TODO

1. feature flags for rabbitmq and db
