import pymongo
from pymongo import MongoClient
from os import environ

db = None


def connect():
    try:
        if (environ.get('APP_ENVIRONMENT') == 'development'):
            mongo_url = "locahost:27017"
        else:
            mongo_url = "mongodb+srv://"+environ.get("SIMPLESEARCH_DB_USERNAME")+":"+environ.get(
                "SIMPLESEARCH_DB_PASSWORD")+"@tattle-data-fkpmg.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
        cli = MongoClient(mongo_url)
        db = cli[environ.get("SIMPLESEARCH_DB_NAME")]
        print('Success Connecting to MongoDB')

    except Exception as e:
        print('Error Connecting to MongoDB')
