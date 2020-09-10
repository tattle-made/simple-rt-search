from os import environ
import pika
import json
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
load_dotenv()
import datetime

from helper import get_video_hash_from_s3_file, get_image_hash_from_s3_file, get_audio_hash_from_s3_file

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

mimetype_collection_map = {
  'image': 'images',
  'video': 'videos',
  'audio': 'audios'
}

def callback(ch, method, properties, body):
    print("MESSAGE RECIEVED %r" % body)
    payload = json.loads(body)
    mimetype = payload['media_type']

    try:
        print('hello')
        if mimetype == 'image':
            media_hash, success = get_image_hash_from_s3_file(payload['file_name'], payload['bucket_name'], payload['filepath_prefix'])
        elif mimetype == 'video':
            media_hash, success = get_video_hash_from_s3_file(payload['file_name'], payload['bucket_name'], payload['filepath_prefix'])
        elif mimetype == 'audio':
            media_hash, success = get_audio_hash_from_s3_file(payload['file_name'], payload['bucket_name'], payload['filepath_prefix'])

        print(media_hash, success)

        if success == True:
            document_to_be_indexed = {
                "hash": media_hash,
                "metadata": payload['metadata'],
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow()
            }

            id = str(store_hash_in_db(mimetype_collection_map[mimetype], document_to_be_indexed))

            print(document_to_be_indexed)
            print(id)

            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print('Error indexing media ', e)


channel.basic_consume(queue='simple-search-index-queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C ')
channel.start_consuming()

