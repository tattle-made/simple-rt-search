from flask_restful import Resource

class Health(Resource):
    def get(self):
        return {'health' : 'green'}
