import pika

credentials = pika.PlainCredentials('user', 'Fn0ukDQVyC')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='my-release-rabbitmq.default.svc', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
