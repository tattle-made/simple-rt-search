from flask_restful import Resource, reqparse
from flask import jsonify
import werkzeug
from hash_helper import get_video_hash_from_local_file, get_image_hash_from_local_file, get_audio_hash_from_local_file
import pymongo
from pymongo import MongoClient

class Search(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        file = args['file']
        file.save('.input/' + file.filename)
        
        hash = get_image_hash_from_local_file(file.filename)
        print(hash)

        mongo_url = "mongodb://localhost:27017"   
        cli = MongoClient(mongo_url)
        print(cli)

        db = cli['simple-rt-search']
        coll = db['sources']
        print('coll : ', coll)
        print('count : ', coll.count_documents)
        if coll.count_documents({}) > 0:
            print(coll) 
        else:
            print("Error accessing Mongo collection")
        return 'hello'