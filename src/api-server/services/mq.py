from os import environ
import pika
import json


class MQ():
    def __init__(self):
        pass

    def connect(self):
        try:
            credentials = pika.PlainCredentials(
                environ.get('MQ_USERNAME'),
                environ.get('MQ_PASSWORD'))
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=environ.get('MQ_HOST'),
                    credentials=credentials
                ))
            self.channel = connection.channel()
            print('Success Connecting to RabbitMQ')
        except Exception as e:
            print('Error Connecting to RabbitMQ ', e)

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
