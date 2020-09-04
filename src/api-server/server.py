from flask import Flask
from flask_restful import Resource, Api
from resources.media import Media

app = Flask(__name__)
# https://flask-restful.readthedocs.io/en/latest/reqparse.html#error-handling
app.config['BUNDLE_ERRORS'] = True

api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'msg': 'hello'}


api.add_resource(HelloWorld, '/')
api.add_resource(Media, '/media')

if __name__ == '__main__':
    app.run(debug=True)
