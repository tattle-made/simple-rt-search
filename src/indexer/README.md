# Indexer

an always on rabbit mq consumer that generates hashes of images and videos and stores them in an elastic search

v 0.0.6

```
docker build -t indexer-test .
docker run -v $(pwd):/app indexer-test
```
