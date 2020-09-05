from flask_restful import Resource, reqparse
from flask import jsonify
import werkzeug
from hash_helper import get_video_hash_from_local_file, get_image_hash_from_local_file, get_audio_hash_from_local_file
import pymongo
from pymongo import MongoClient
import pprint

print('initializing db')
mongo_url = "mongodb://db:27017/"   
client = MongoClient(mongo_url)
db = client['simple-rt-search']

class Search(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        file = args['file']
        file.save('.input/' + file.filename)
        mimetype = file.mimetype
        
        image_hash, result = get_image_hash_from_local_file(file.filename)
        print(image_hash)

        if mimetype.startswith('image/'):
            print('file is image')
            media_hash, success = get_image_hash_from_local_file(file.filename)
            print(media_hash, success)
            images = db['images']
            if success == True:
                results = images.find({"hash":media_hash})
        elif mimetype.startswith('video/'):
            print('file is video')
            media_hash, success = get_video_hash_from_local_file(file.filename)
            videos = db['videos']
            if success == True:
                results = videos.find({"hash":media_hash})
        elif mimetype.startswith('audio/'):
            print('file is audio')
            media_hash, success = get_audio_hash_from_local_file(file.filename)
            audios = db['audios']
            if success == True:
                results = audios.find({"hash":media_hash})
        else :
            success = false
            
        print(results, success)

        if success == True:
            response = []
            for result in results:
                del result['_id'] 
                response.append(result)
                
        print(response)
        
        return response, 200