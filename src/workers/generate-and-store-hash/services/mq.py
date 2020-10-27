from os import environ
import pika
import json


class MQ():
    def __init__(self):
        self.mq_username = environ.get('MQ_USERNAME')
        self.mq_password = environ.get('MQ_PASSWORD')
        self.mq_host = environ.get('MQ_HOST')

    def connect(self):
        try:
            credentials = pika.PlainCredentials(
                self.mq_username,
                self.mq_password)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.mq_host,
                    credentials=credentials
                ))
            self.channel = connection.channel()
            print('Success Connecting to RabbitMQ')
        except Exception as e:
            print('Error Connecting to RabbitMQ ', e)
            raise

    def is_connected(self):
        return self.channel.is_open

    def publish_to_queue(self, queue_name, payload):
        if self.is_connected():
            self.channel.basic_publish(exchange='',
                                       routing_key=queue_name,
                                       properties=pika.BasicProperties(
                                           delivery_mode=2),  # make message persistent
                                       body=json.dumps(payload))
        else:
            raise Exception('Connection Lost. Cannot publish payload')
            


mq = MQ()

def get_mq_instance():
    return mq
