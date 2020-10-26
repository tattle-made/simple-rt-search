import pika
from os import environ
import json
import uuid
import sys
from services.rabbitmq import RabbitMQ


def add_job_to_queue(payload):
    rabbitmq = RabbitMQ.instance()
    if rabbitmq.channel.is_open:
        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='simple-search-index-queue',
            properties=pika.BasicProperties(
                delivery_mode=2),  # make message persistent
            body=json.dumps(payload))
    else:
        rabbitmq.connect()
        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='simple-search-index-queue',
            properties=pika.BasicProperties(
                delivery_mode=2),  # make message persistent
            body=json.dumps(payload))
