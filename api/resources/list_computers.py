## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db
from models.room import Room
from models.computer import Computer

## Our resource for Getting a full list of computers
class ComputerList(Resource):
    request_args = {
        'room': fields.String(),
        'detailed_response': fields.Bool()
    }

    ## GET method endpoint
    @use_args(request_args)
    def get(self, args):
        if 'room' in args:
            print(args['room'])
            if args['room'] != 'Not Set' and args['room'] != 'not set':
                ## Check the room exists
                room = Room.query.filter_by(room_name=args['room']).first()
                if room is None:
                    abort(404, message="Room not found")
            ## Get a list of all our machines
            computers = Computer.query.all()
            computerArray = []
            if computers is not None:
                now = datetime.now()
                for computer in computers:
                    computer.updateStatus(now)
                    if args['room'] == 'Not Set' or args['room'] == 'not set':
                        ## If the detailed response flag is present
                        if 'detailed_response' in args:
                            ## Check if the response wants full details or trimmed responses
                            if args['detailed_response'] == True:
                                computerArray.append(computer.serialize)
                            else:
                                computerArray.append(computer.trimmed_serialize)
                        else:
                            computerArray.append(computer.trimmed_serialize)
                    else:
                        if computer.room_name == args['room']:
                            ## If the detailed response flag is present
                            if 'detailed_response' in args:
                                ## Check if the response wants full details or trimmed responses
                                if args['detailed_response'] == True:
                                    computerArray.append(computer.serialize)
                                else:
                                    computerArray.append(computer.trimmed_serialize)
                            else:
                                computerArray.append(computer.trimmed_serialize)
                    db.session.commit()
            ## Generate our response
            response = {
                "meta": {},
                "links": {
                    "self": request.url
                },
                "data": {
                    "computers": computerArray
                }
            }
            return jsonify(response)
        else:
            ## Get a list of all our machines
            computers = Computer.query.all()
            computersArray = []
            ## Check we found any computers
            if computers is not None:
                now = datetime.now()
                for computer in computers:
                    computer.updateStatus(now)
                db.session.commit()
                computerArray = []
                ## Check if the response wants full details or trimmed responses
                if 'detailed_response' in args:
                    ## Check if the response wants full details or trimmed responses
                    if args['detailed_response'] == True:
                        computerArray = [computer.serialize for computer in computers]
                    else:
                        computerArray = [computer.trimmed_serialize for computer in computers]
                else:
                    computerArray = [computer.trimmed_serialize for computer in computers]
            ## Generate our response
            response = {
                "meta": {},
                "links": {
                    "self": request.url
                },
                "data": {
                    "computers": computerArray
                }
            }
            return jsonify(response)
