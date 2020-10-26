from services.mongo import Mongo
from helper import get_video_hash_from_s3_file, get_image_hash_from_s3_file, get_audio_hash_from_s3_file
import logging
from datetime import datetime
import sys
from os import environ
import pika
import json
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
load_dotenv()

mongo = Mongo.instance()

try:
    credentials = pika.PlainCredentials(environ.get(
        'MQ_USERNAME'), environ.get('MQ_PASSWORD'))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='simple-search-index-queue', durable=True)
    q = channel.queue_declare(
        queue='simple-search-index-queue', durable=True, passive=True)
    channel.queue_declare(queue='simple-search-report-queue', durable=True)
    print('Success Connecting to RabbitMQ')
except Exception as e:
    print('Error Connecting to RabbitMQ', e)


def store_hash_in_db(collection_name, doc):
    global mongo
    print(mongo)
    print(mongo.db)
    try:
        doc_id = mongo.db[collection_name].insert_one(doc).inserted_id
        return doc_id
    except Exception as e:
        print('error storing hash in db', e)
        raise


mimetype_collection_map = {
    'image': 'images',
    'video': 'videos',
    'audio': 'audios'
}


def callback(ch, method, properties, body):
    print("MESSAGE RECEIVED %r" % body)
    payload = json.loads(body)
    report = {}
    report["source_id"] = payload["source_id"]
    report["source"] = payload["source"]
    mimetype = payload['media_type']

    try:
        print("Generating media hash ...")
        if mimetype == 'image':
            media_hash, success = get_image_hash_from_s3_file(
                payload['file_name'], payload['bucket_name'], payload['filepath_prefix'])
        elif mimetype == 'video':
            media_hash, success = get_video_hash_from_s3_file(
                payload['file_name'], payload['bucket_name'], payload['filepath_prefix'])
        elif mimetype == 'audio':
            media_hash, success = get_audio_hash_from_s3_file(
                payload['file_name'], payload['bucket_name'], payload['filepath_prefix'])

        print(media_hash, success)
        timestamp = str(datetime.utcnow())
        if success == True:
            print("Media hash generated successfully")
            document_to_be_indexed = {
                "hash": media_hash,
                "metadata": payload['metadata'],
                "created_at": timestamp,
                "updated_at": timestamp
            }
            print("Storing hash in Simple Search db ...")
            index_id = str(store_hash_in_db(
                mimetype_collection_map[mimetype], document_to_be_indexed))
            print("Sending report to queue ...")
            report["index_timestamp"] = timestamp
            report["index_id"] = index_id
            report["status"] = "indexed"

            channel.basic_publish(exchange='',
                                  routing_key='simple-search-report-queue',
                                  properties=pika.BasicProperties(
                                      content_type='application/json',
                                      delivery_mode=2),  # make message persistent
                                  body=json.dumps(report))

            print("Indexing success report sent to report queue")
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print('Error indexing media ', e)
        print("Media hashing failed")
        print("Sending report to queue ...")
        report["status"] = "failed"
        report["failure_timestamp"] = str(datetime.utcnow())

        channel.basic_publish(exchange='',
                              routing_key='simple-search-report-queue',
                              properties=pika.BasicProperties(
                                  content_type='application/json',
                                  delivery_mode=2),  # make message persistent
                              body=json.dumps(report))
        print("Indexing failure report sent to report queue")
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='simple-search-index-queue',
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C ')
channel.start_consuming()
