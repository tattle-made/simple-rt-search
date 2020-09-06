import pika
from os import environ
import json

credentials = pika.PlainCredentials(environ.get(
    'MQ_USERNAME'), environ.get('MQ_PASSWORD'))
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='simple-search-index-queue', durable=True)

def add_job_to_queue(payload):
    channel.basic_publish(exchange='', routing_key='simple-search-index-queue', body=json.dumps(payload))
    # connection.close()
