## Imports
from datetime import datetime
from flask_restful import Resource
from flask_jsonpify import jsonify
from shared import db

## Our template resource
class TemplateResource(Resource):
    def get(self):
        return jsonify([])
