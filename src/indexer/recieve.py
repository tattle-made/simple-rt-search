from os import environ
import pika
import json
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
load_dotenv()


credentials = pika.PlainCredentials(environ.get(
    'MQ_USERNAME'), environ.get('MQ_PASSWORD'))
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='simple-search-index-queue', durable=True)


print('initializing db')
mongo_url = "mongodb://db:27017"
client = MongoClient(mongo_url)
db = client['simple-rt-search']

def store_hash_in_db(collection_name, doc):
  try:
    doc_id = db[collection_name].insert_one(doc).inserted_id
    print('doc id : ', doc_id)
    return doc_id
  except Exception as e:
    print('error storing hash in db')
    raise

mimetyp_collection_map = {
  'image': 'images',
  'video': 'videos',
  'audio': 'audios'
}

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    payload = json.loads(body)
    print(payload)
    print(type(payload))
    mimetype = payload.metadata.media_type

    payload["created_at"]: datetime.datetime.utcnow()
    payload["updated_at"]: datetime.datetime.utcnow()
    doc_id = store_hash_in_db(mimetyp_collection_map[mimetype], doc)
    response = {
        'doc_id': str(doc_id)
    }
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='simple-search-index-queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C ')
channel.start_consuming()

