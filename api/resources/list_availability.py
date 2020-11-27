## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db
from models.computer import Computer
from models.room import Room

## Our resource for getting the availability of the machines in a room
class AvailabilityList(Resource):
    ## The URL parameters the REST API endpoints can recieve and parse for use
    get_args = {
        'room': fields.String(required=True)
    }

    @use_args(get_args)
    def get(self, args):
        ## Check the room exists
        room = Room.query.filter_by(room_name=args['room']).first()
        if room is None:
            abort(404, message="Room not found")
        ## Get a list of all our machines
        machines = Computer.query.all()
        availabilityArray = []
        ## Check we found any machines
        if machines is not None:
            for computer in machines:
                ## Check if the PC is in the desired room
                if computer.room_name == args['room']:
                    ## Create an json object to be added to the response array
                    computerAvailability = {
                        "id": computer.identifier,
                        "desk": computer.desk_number,
                        "mac_address": computer.mac_address,
                        "machine_name": computer.machine_name,
                        "availability_status": computer.checkAvailability()
                    }
                    availabilityArray.append(computerAvailability)
        ## Generate our JSON response
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "availability": availabilityArray
            }
        }
        ## Return our JSON response
        return jsonify(response)
