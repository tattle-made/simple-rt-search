from flask import Flask
from flask_restful import Resource, Api
from resources.media import Media
from resources.search import Search

app = Flask(__name__)
# https://flask-restful.readthedocs.io/en/latest/reqparse.html#error-handling
app.config['BUNDLE_ERRORS'] = True

api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'msg': 'hello 2'}


api.add_resource(HelloWorld, '/')
api.add_resource(Media, '/media')
api.add_resource(Search, '/search')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
