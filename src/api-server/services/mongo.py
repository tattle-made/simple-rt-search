import pymongo
from pymongo import MongoClient
from os import environ

db = None


def connect():
    try:
        mongo_url = environ.get('SIMPLESEARCH_MONGO_URL')
        cli = MongoClient(mongo_url)
        db = cli[environ.get("SIMPLESEARCH_DB_NAME")]
        print('Success Connecting to MongoDB')

    except Exception as e:
        print('Error Connecting to MongoDB')
