import os
import re
from dotenv import load_dotenv
load_dotenv()
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import json
import requests
import random
import logging
import re
from os import environ
import pika
from bson import ObjectId

mongo_url = "mongodb+srv://"+os.environ.get("SHARECHAT_DB_USERNAME")+":"+os.environ.get("SHARECHAT_DB_PASSWORD")+"@tattle-data-fkpmg.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"   
cli = MongoClient(mongo_url)
db = cli[os.environ.get("SHARECHAT_DB_NAME")]
coll = db[os.environ.get("SHARECHAT_DB_COLLECTION")]

credentials = pika.PlainCredentials(environ.get(
    'MQ_USERNAME'), environ.get('MQ_PASSWORD'))
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='simple-search-report-queue', durable=True)

def callback(ch, method, properties, body):
    print("MESSAGE RECEIVEDr %" % body)
    try:
        payload = json.loads(body)
        report = {}
        if payload["status"] == "indexed":
            report["status"] = payload["status"]
            report["index_timestamp"] = payload["index_timestamp"]
            report["index_id"] = payload["index_id"]
            coll.update_one(
                {"_id": ObjectId(payload["source_id"])},
                {"$set": {"simple_search.indexer_status": report}})
        elif payload["status"] == "failed":
            report["status"] = payload["status"]
            report["failure_timestamp"] = payload["failure_timestamp"]
            coll.update_one(
                {"_id": ObjectId(payload["source_id"])},
                {"$set": {"simple_search.indexer_status": report}})
        print("Report uploaded to Mongo")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        print(logging.traceback.format_exc())
        ch.basic_ack(delivery_tag=method.delivery_tag)
    


channel.basic_consume(queue='simple-search-report-queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C ')
channel.start_consuming()

