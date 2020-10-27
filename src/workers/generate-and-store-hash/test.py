from controllers.mongo_controller import mongo_controller
from datetime import datetime

try:
    mongo_controller.connect()
except Exception as e:
    print('Error connecting to Mongo')
    exit()

timestamp = str(datetime.utcnow())
document_to_be_indexed = {
    "hash": 'abcdef',
    "metadata": {"a":'test', "b":1},
    "created_at": timestamp,
    "updated_at": timestamp
}
print("Storing hash in Simple Search db ...")
index_id = mongo_controller.store_hash_doc('images', document_to_be_indexed)

print(index_id)