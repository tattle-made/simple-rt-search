from controllers.queue_controller import queue_controller
from controllers.mongo_controller import mongo_controller
from helper import get_video_hash_from_s3_file, get_image_hash_from_s3_file, get_audio_hash_from_s3_file
import logging
from datetime import datetime, timedelta
from time import perf_counter
import sys
from os import environ
import pika
import json
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
load_dotenv()
import logging

try:
    queue_controller.connect()
    queue_controller.declare_queues()
except Exception as e:
    print('Error Connecting to or Declaring Queues')
    print(logging.traceback.format_exc())
    exit()

try:
    mongo_controller.connect()
except Exception as e:
    print('Error connecting to Mongo')
    exit()

mimetype_collection_map = {
    'image': 'images',
    'video': 'videos',
    'audio': 'audios'
}


def callback(ch, method, properties, body):
    # print("MESSAGE RECEIVED %r" % body)
    print("MESSAGE RECEIVED")
    start = perf_counter()
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

        # print(media_hash, success)
        print("Hash: ", media_hash)
        timestamp = str(datetime.utcnow())
        if success == True:
            print("Media hash generated successfully")
            document_to_be_indexed = {
                "hash": media_hash,
                "metadata": payload['metadata'],
                "created_at": timestamp,
                "updated_at": timestamp,
                "source": payload["source"],
                "source_id": payload["source_id"]
            }
            print("Storing hash in Simple Search db ...")
            index_id = mongo_controller.store_hash_doc(mimetype_collection_map[mimetype], document_to_be_indexed)
            delta = perf_counter() - start 
            print("Time taken: ", delta)
            print("Sending report to queue ...")
            
            report["index_timestamp"] = timestamp
            report["index_id"] = index_id
            report["status"] = "indexed"
            queue_controller.add_data_to_report_queue(report)
            
            print("Indexing success report sent to report queue")
            print("")
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(logging.traceback.format_exc())
        print('Error indexing media ', e)
        print("Media hashing failed")
        print("Sending report to queue ...")
        report["status"] = "failed"
        report["failure_timestamp"] = str(datetime.utcnow())

        queue_controller.add_data_to_report_queue(report)
        print("Indexing failure report sent to report queue")
        ch.basic_ack(delivery_tag=method.delivery_tag)

queue_controller.start_consuming('simple-search-index-queue', callback)




