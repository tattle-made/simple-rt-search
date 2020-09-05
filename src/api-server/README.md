# API Server

an always on rabbit mq consumer that generates hashes of images and videos and stores them in an elastic search

v 0.0.1

```
docker build -t simple-rt-search-api .
docker run -v $(pwd):/app --name simple-rt-search-api -p 5000:5000 simple-rt-search-api
```
