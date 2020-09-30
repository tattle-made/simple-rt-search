import pika
from os import environ

credentials = pika.PlainCredentials(environ.get('MQ_USERNAME'), environ.get('MQ_PASSWORD'))
connection = pika.BlockingConnection(pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='test')

def callback(ch, method, properties, body):
    print('MESSAGE RCVD %r' % body)

channel.basic_consume(queue='test', on_message_callback=callback)