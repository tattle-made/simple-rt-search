from flask_restful import Resource, reqparse
from flask import jsonify
import werkzeug
from hash_helper import get_video_hash_from_local_file, get_image_hash_from_local_file, get_audio_hash_from_local_file
import pymongo
from pymongo import MongoClient
import pprint
from os import environ

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


class Search(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'file', type=werkzeug.datastructures.FileStorage, location='files')
            args = parser.parse_args()
            print(args)
            file = args['file']
            file.save('.input/' + file.filename)
            mimetype = file.mimetype
            print(mimetype)
            if mimetype.startswith('image/'):
                print('file is image')
                media_hash, success = get_image_hash_from_local_file(
                    file.filename)
                print(media_hash, success)
                images = db['images']
                if success == True:
                    results = images.find({"hash": media_hash})
            elif mimetype.startswith('video/'):
                print('file is video')
                media_hash, success = get_video_hash_from_local_file(
                    file.filename)
                print(media_hash, success)
                videos = db['videos']
                if success == True:
                    results = videos.find({"hash": media_hash})
            elif mimetype.startswith('audio/'):
                print('file is audio')
                media_hash, success = get_audio_hash_from_local_file(
                    file.filename)
                audios = db['audios']
                if success == True:
                    results = audios.find({"hash": media_hash})
            else:
                success = False
                results = []

            print(results, success)

            if success == True:
                response = []
                for result in results:
                    del result['_id']
                    del result['created_at']
                    del result['updated_at']
                    response.append(result)
                return response, 200
            else:
                return 'Error generating hash', 500

        except Exception as e:
            print(e)
            return 'error in search '+str(e), 500
