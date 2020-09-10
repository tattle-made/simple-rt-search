```
docker exec -it rabbitmq rabbitmq-plugins enable rabbitmq_management
docker exec -it simple-rt-indexer /bin/sh
```

# Starting Dev environment

REMEMBER to modify the Dockerfiles for indexer and api-server if you plan to actively develop features.
I usually replace the last line of the Dockerfiles with `CMD tail -f /dev/null`. Then I run the server and indexers from within the containers in debug mode.

run `docker-compose up` and verify if all the services are up. The first time you do this, it will take 5-7 minutes
for all services to come up. Its usually instantaneous after that, as long as you don't make changes to the Dockerfile associated
with each service.

mongo : visit http://localhost:27017

mongo UI : visit http://localhost:8081

rabbitmq UI : visit http://localhost:15672

search server : visit http://localhost:5000
