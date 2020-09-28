import pika
from os import environ
import json
import uuid
import sys
class IndexMedia(object):
    def __init__(self):
        self.credentials = pika.PlainCredentials(environ.get('MQ_USERNAME'), environ.get('MQ_PASSWORD'))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=self.credentials))
        self.channel = self.connection.channel()

        self.channel.basic_consume(
            queue='amq.rabbitmq.reply-to',
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response=body

    def add_job_to_queue(self, payload):
        self.response=None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='', 
            routing_key='simple-search-index-queue', 
            properties=pika.BasicProperties(
                reply_to='amq.rabbitmq.reply-to',
                correlation_id=self.corr_id,
                delivery_mode=2 # make message persistent
            ),
            body=json.dumps(payload))

        while self.response is None:
            self.connection.process_data_events()
        self.channel.queue_declare('simple-search-report-queue', durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key='simple-search-report-queue',
            body=json.dumps(self.response.decode('utf-8')).replace('"{','{').replace('}"','}').replace('\\',''),
            properties=pika.BasicProperties(delivery_mode=2))

        return self.response
        # return json.dumps(self.response.decode('utf-8'))
    # connection.close()
