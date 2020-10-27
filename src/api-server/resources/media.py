from flask_restful import Resource, reqparse
import werkzeug
import json
from flask import jsonify, request
from send import add_job_to_queue
import datetime


class Media(Resource):
    def __init__(self):
        self.post_request_parser = reqparse.RequestParser()
        self.post_request_parser.add_argument(
            'file_url', type=str, help='file url is a mandatory field')
        self.post_request_parser.add_argument('file_name', type=str)
        self.post_request_parser.add_argument('bucket_name', type=str)
        self.post_request_parser.add_argument('filepath_prefix', type=str)
        self.post_request_parser.add_argument('media_type', type=str, choices=(
            'video', 'audio', 'image'), help='The file type of media item. Acceptable values : video, image, audio', required=True)
        self.post_request_parser.add_argument('source', type=str)
        self.post_request_parser.add_argument('source_id', type=str)
        self.post_request_parser.add_argument(
            'metadata', type=dict, help='Any metadata that you want to store in the search index. Use Judiciously')

    # TODO add validation for supported mimetypes : image/jpeg, image/png, audio/mpeg, audio/wav, video/mpeg

    def post(self):
        print("Server received request for queuing media")
        try:
            args = self.post_request_parser.parse_args(strict=True)
            print("Adding requested job to indexing queue ...")
            add_job_to_queue(args)
            print("Job added")
            return 'media enqueued', 200

        except Exception as e:
            return 'Error indexing media : '+str(e), 500
