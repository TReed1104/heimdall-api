## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jsonpify import jsonify
from shared import db
from models.room import Room

## Our resource for Getting a full list of computers
class RoomList(Resource):
    def get(self):
        ## Find the Room
        rooms = Room.query.all()
        roomsResponseArray = []
        if rooms is not None:
            roomsResponseArray = [room.serialize for room in rooms]
        ## Generate our JSON response
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "rooms": roomsResponseArray
            }
        }
        return jsonify(response)
