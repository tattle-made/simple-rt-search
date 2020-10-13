import pika
from os import environ
import json
import uuid
import sys

try:
    print('send.py')
    print(environ.get('MQ_HOST'))
    print(environ.get('MQ_USERNAME'))
    print(environ.get('MQ_PASSWORD'))
    credentials = pika.PlainCredentials(environ.get(
        'MQ_USERNAME'), environ.get('MQ_PASSWORD'))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='simple-search-index-queue', durable=True)
    channel.queue_declare(queue='simple-search-report-queue', durable=True)
    print('Success Connecting to RabbitMQ')
except Exception as e:
    print('Error Connecting to Rabbit MQ', e)


def add_job_to_queue(payload):
    channel.basic_publish(
        exchange='',
        routing_key='simple-search-index-queue',
        properties=pika.BasicProperties(
            delivery_mode=2),  # make message persistent
        body=json.dumps(payload))
