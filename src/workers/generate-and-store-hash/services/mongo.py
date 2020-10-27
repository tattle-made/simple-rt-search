import pymongo
from pymongo import MongoClient
from os import environ

class Mongo():
    def __init__(self):
        self.mongo_url = environ.get('SIMPLESEARCH_MONGO_URL')
        self.db_name = environ.get("SIMPLESEARCH_DB_NAME")

    def connect(self):
        try:
            self.cli = MongoClient(self.mongo_url)
            self.db = self.cli[self.db_name]
            print('Success Connecting to MongoDB')
        except Exception as e:
            print('Error Connecting to MongoDB', e)
            raise

    def write(self, collection_name, document):
        try:
            doc_id = self.db[collection_name].insert_one(document).inserted_id
            return str(doc_id)
        except Exception as e:
            print('error storing hash in db', e)
            raise

    # condition ex : {"hash": media_hash}
    def find(self, collection_name, condition):
        collection = db[collection_name]
        return collection.find(condition)

db = Mongo()

def get_db_instance():
    return db