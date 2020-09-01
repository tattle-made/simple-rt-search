import pika

credentials = pika.PlainCredentials('user', 'RQnPmtV388')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='my-release-rabbitmq.default.svc', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='simple-search-index-queue', durable=True)

channel.basic_publish(
    exchange='', routing_key='simple-search-index-queue', body='Hello World!')
connection.close()
