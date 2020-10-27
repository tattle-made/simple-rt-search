# Simple Realtime Search is a fast easy to scale tool to make media files searchable

Fact Checkers and Journalists fighting misinformation need a reliable way to store and search millions of images, audios and videos circulating on chat apps and social media.
Since a lot of this data is often recirculated and re-shared without any major modifications, simple hashing techniques can be used to provide unique signatures to them. Being able
to associate simple metadata to these posts can help lay the foundation for building realtime automated service and products on top of this data.
We are building Simple Realtime Search Service just for that.

## Example Application

![Gif showing search via images](https://tattle-media.s3.amazonaws.com/khoj-demo.gif)

## Features

- Realtime search results
- Easy to scale if you anticipate increased loads during periods of high activity
- Easy to install and run on your own
- Support for installation and new feature development for your organization

## Immediate Roadmap

| In Progress   | Up next   | On the Horizon | Completed                                   |
| ------------- | --------- | -------------- | ------------------------------------------- |
| Documentation | Admin UI  | Admin UI       | Video Indexing and Search                   |
|               | Demo apps | Basic Auth     | Image Indexing and Search                   |
|               |           |                | Audio Indexing and Search                   |
|               |           |                | Integrate RabbitMQ to implement a Job Queue |
|               |           |                | Integrate Flask RESTful to make API         |

## Running Locally

Run `docker-compose up`

This will bring up the following services :

1. Mongo DB : used to store media hash and any associated metadata with the media.
2. Mongo UI : a UI to debug and monitor changes to the mongo db. Only meant for debugging purposes and not for production.
3. RabbitMQ : Used as a Job Queue to queue up long media indexing jobs.
4. Indexer : A RabbitMQ consumer that receives any new jobs that are added to the queue and processes them.
5. Search Server : a public REST API to index new media and provide additional public APIs to interact with this service.

The first time you run `docker-compose up` it will take 5-7 minutes for all services to come up. Its usually instantaneous after that, as long as you don't make changes to the Dockerfile associated
with each service. To verify if every service is up, visit the following URLs

mongo : visit http://localhost:27017

mongo UI : visit http://localhost:8081

rabbitmq UI : visit http://localhost:15672

search server : visit http://localhost:5000

Since a lot of the underlying media processing libraries are platform specific, I usually prefer developing from within the docker container to avoid any pre deployment surprises.
I replace the last line of the Dockerfiles with `CMD tail -f /dev/null`. Then I run the server and indexers from within the containers in debug mode.
This might be slightly unorthodox but it ensures that what I develop on my local machine can be deployed within a docker container as I am developing it.

# Handy Shortcuts

```
docker exec -it rabbitmq rabbitmq-plugins enable rabbitmq_management
docker exec -it simple-rt-indexer /bin/sh
```

```
# index in a kubernetes cluster
curl -H "Content-Type: application/json" -X POST -v --data '{"file_url":"https://tattle-media.s3.amazonaws.com/test-data/videos/cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4","media_type":"video","bucket_name":"tattle-media", "file_name":"cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4", "filepath_prefix":"test-data/videos/" ,"source":"khoj, "source_id":"23423423432","metadata":{}}' http://service-tattle-simplesearch-rest/media
# index normally
curl -H "Content-Type: application/json" -X POST -v --data '{"file_url":"https://tattle-media.s3.amazonaws.com/test-data/videos/cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4","media_type":"video","bucket_name":"tattle-media","file_name":"cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4","filepath_prefix":"test-data/videos/","source":"khoj","source_id":"23423423432","metadata":{}}' http://localhost:5000/media
curl -H "Content-Type: application/json" -X POST -v --data '{"file_url":"https://tattle-media.s3.amazonaws.com/test-data/images/004e0126-2ef6-41de-97be-e0b9daaee480.jpeg","media_type":"image","bucket_name":"tattle-media","file_name":"004e0126-2ef6-41de-97be-e0b9daaee480.jpeg","filepath_prefix":"test-data/images/","source":"khoj","source_id":"23423423432","metadata":{}}' http://localhost:5000/media
```

# Caveat

We find that the pip-compile step takes too long to finish during docker build. So we find it useful to generate it locally on our machines and check in accurate requirements.txt file in the git repo

## Want to contribute?

We have a [guide](CONTRIBUTING.md) for you.

## To get help with developing or running Simple Search Server

Join our [slack channel](https://join.slack.com/t/tattle-workspace/shared_invite/zt-da07n75v-kIw9Z5b~_gDKP~JsScP1Vg) to get someone to respond to immediate doubts and queries.

## Want to get help deploying it into your organisation?

contact us at admin@tattle.co.in
