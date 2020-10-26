from os import environ
import pika


class RabbitMQ():
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating New Instance')
            cls._instance = cls.__new__(cls)
            try:
                credentials = pika.PlainCredentials(
                    environ.get('MQ_USERNAME'),
                    environ.get('MQ_PASSWORD'))
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=environ.get('MQ_HOST'),
                        credentials=credentials
                    ))
                cls._instance.channel = connection.channel()
                cls._instance.channel.queue_declare(
                    queue='simple-search-index-queue', durable=True)
                cls._instance.channel.queue_declare(
                    queue='simple-search-report-queue', durable=True)
                print('Success Connecting to RabbitMQ')
            except Exception as e:
                print('Error Connecting to RabbitMQ ', e)
        return cls._instance

    def connect(self):
        credentials = pika.PlainCredentials(
            environ.get('MQ_USERNAME'),
            environ.get('MQ_PASSWORD'))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=environ.get('MQ_HOST'),
                credentials=credentials
            ))
        self.channel = connection.channel()
        self.channel.queue_declare(
            queue='simple-search-index-queue', durable=True)
        self.channel.queue_declare(
            queue='simple-search-report-queue', durable=True)
