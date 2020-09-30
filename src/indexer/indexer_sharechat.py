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
import mimetypes
from helper_sharechat import get_data, index_media
import logging
import re

mongo_url = "mongodb+srv://"+os.environ.get("SHARECHAT_DB_USERNAME")+":"+os.environ.get("SHARECHAT_DB_PASSWORD")+"@tattle-data-fkpmg.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"   
cli = MongoClient(mongo_url)
db = cli[os.environ.get("SHARECHAT_DB_NAME")]
coll = db[os.environ.get("SHARECHAT_DB_COLLECTION")]

def IndexerSharechat():
    c=0
    end = datetime.utcnow() 
    start = end - timedelta(days=1)
    for i in coll.find({
        "media_type": {"$in": ["image", "video"]}, 
        "scraped_date": {'$gte':start,'$lt':end}}).limit(500): #limit for testing
        try:
            print(i["_id"])
            res = {}
            data = get_data(i)

            response = index_media(str(data))
            res["response_timestamp"] = str(datetime.utcnow())
            res["response_text"] = json.loads(response) 

            coll.update_one(
                {"_id": i["_id"]},
                {"$set": {"simple_search.rabbitmq_status": res}})
            c+=1
        except Exception as e:
            print(logging.traceback.format_exc())
            print('Error queueing data', e)
    print("Sent {} records to queue".format(c))
    return c


if __name__ == "__main__":
    IndexerSharechat()
