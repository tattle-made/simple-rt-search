import pika
from os import environ

credentials = pika.PlainCredentials(environ.get('MQ_USERNAME'), environ.get('MQ_PASSWORD'))
connection = pika.BlockingConnection(pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='test')

channel.basic_publish(exchange='', routing_key='test', body='Hello World!')
print('sent hello world')