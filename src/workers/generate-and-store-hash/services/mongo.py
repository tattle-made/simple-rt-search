import pymongo
from pymongo import MongoClient
from os import environ


class Mongo():
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            print('Connecting to MongoDB')
            try:
                if (environ.get('APP_ENVIRONMENT') == 'development'):
                    mongo_url = "mongodb://db:27017/"

                else:
                    mongo_url = "mongodb+srv://"+environ.get("SIMPLESEARCH_DB_USERNAME")+":"+environ.get(
                        "SIMPLESEARCH_DB_PASSWORD")+"@tattle-data-fkpmg.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

                cli = MongoClient(mongo_url)
                cls._instance.db = cli[environ.get("SIMPLESEARCH_DB_NAME")]

                print('Success Connecting to MongoDB')
            except Exception as e:
                print('Error Connecting to MongoDB ', e)
        return cls._instance
