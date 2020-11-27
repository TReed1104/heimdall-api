## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db
from models.room import Room
from models.desk import Desk

## Our resource for Getting a full list of computers
class DeskList(Resource):
    request_args = {
        'room_id': fields.Integer(),
        'room_name': fields.String()
    }

    ## GET method endpoint
    @use_args(request_args)
    def get(self, args):
        if 'room_id' not in args and 'room_name' not in args:
            ## Find all the rooms in the system
            desks = Desk.query.all()
            deskArray = []
            if desks is not None:
                deskArray = [desk.serialize for desk in desks]
                ## Generate our JSON response
            response = {
                "meta": {},
                "links": {
                    "self": request.url
                },
                "data": {
                    "desks": deskArray
                }
            }
            return jsonify(response)
        else:
            room = None
            if 'room_id' in args:
                room = Room.query.filter_by(identifier=args['room_id']).first()
            elif 'room_name' in args:
                room = Room.query.filter_by(room_name=args['room_name']).first()
            else:
                abort(422, message='Invalid Parameters')
            ## Check we found a room
            if room is None:
                abort(404, message="Room not found")
            ## Get a list of all our Desks
            desks = Desk.query.filter_by(room_id=room.identifier).all()
            desksReponseArray = []
            if desks is not None:
                desksReponseArray = [desk.serialize for desk in desks]
            ## Generate our JSON response
            response = {
                "meta": {},
                "links": {
                    "self": request.url
                },
                "data": {
                    "desks": desksReponseArray
                }
            }
            return jsonify(response)
