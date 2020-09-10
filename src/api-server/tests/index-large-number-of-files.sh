#!/bin/bash
for i in {1..333}
do
   curl -H "Content-Type: application/json" -X POST -v --data '{"file_url":"https://tattle-media.s3.amazonaws.com/test-data/videos/cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4","media_type":"video","bucket_name":"tattle-media", "file_name":"cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4", "filepath_prefix":"test-data/videos/" ,"metadata":{"source":"khoj","source_id":23423423432}}' http://localhost:5000/media
done