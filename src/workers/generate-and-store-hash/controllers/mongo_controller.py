from services.mongo import get_db_instance

class MongoController():
    def __init__(self):
        self.db = get_db_instance()

    def connect(self):
        self.db.connect()

    def store_hash_doc(self, collection_name, document):
        return self.db.write(collection_name, document)

    def find_matching_hash(self, collection_name, document):
        return self.find(collection_name, document)

mongo_controller = MongoController()