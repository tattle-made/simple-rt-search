from flask_restful import Resource, reqparse
import werkzeug
import json
from flask import jsonify, request
from hash_helper import get_video_hash_from_local_file, get_image_hash_from_local_file, get_audio_hash_from_local_file

class Media(Resource):
    def get(self):
        return {'name': 'media'}
    
    # TODO add validation for supported mimetypes : image/jpeg, image/png, audio/mpeg, audio/wav, video/mpeg
    def post(self):
        # handle file
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        file = args['file']
        file.save(file.filename)

        hash = get_video_hash_from_local_file(file.fileName)
        print(hash)

        # handle metadata
        # TODO : find a way to do this using reqparse.RequestParser
        metadata_form = request.form.to_dict(flat=False).get('metadata')[0]
        metadata = json.loads(metadata_form) 
        print(metadata)
        
        
        
        
        
        
        
        
        
        
        
