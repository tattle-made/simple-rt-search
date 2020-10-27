import pika
from os import environ

credentials = pika.PlainCredentials(environ.get('MQ_USERNAME'), environ.get('MQ_PASSWORD'))
connection = pika.BlockingConnection(pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='test', durable=True)

channel.queue_declare(queue='test-response', durable=True)

def callback(ch, method, properties, body):
    print('MESSAGE RCVD %r' % body)
    channel.basic_publish(exchange='', routing_key='test-response', body='Hello World! response')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='test', on_message_callback=callback)
print("receiving message")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
