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
from models.computer import Computer

class ComputerHandler(Resource):
    ## The URL arguments the REST API endpoints can recieve and parse
    get_and_delete_args = {
        'id': fields.Integer(required=True)
    }
    post_args = {
        'mac_address': fields.String(required=True),
        'machine_name': fields.String(required=True),
        'ip_address': fields.String(required=True),
        'os_name': fields.String(required=True),
        'os_release': fields.String(required=True),
        'os_build': fields.String(required=True),
        'room': fields.String(),
        'desk': fields.String()
    }
    put_args = {
        'mac_address': fields.String(required=True),
        'machine_name': fields.String(),
        'ip_address': fields.String(),
        'os_name': fields.String(),
        'os_release': fields.String(),
        'os_build': fields.String(),
        'room': fields.String(),
        'desk': fields.String()
    }

    ## The Get Verb Method
    @use_args(get_and_delete_args)
    def get(self, args):
        ## Find the machine
        machine = Computer.query.filter_by(identifier=args['id']).first()
        ## check we found a machine
        if machine is None:
            abort(404, message="Computer not found")
        ## We've found a machine, serialise it into a json format for the response
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "computer": machine.serialize
            }
        }
        return jsonify(response)

    ## The Post Verb Method
    @use_args(post_args)
    def post(self, args):
        ## Check the mutually inclusive optional parameters
        if ('room' in args and 'desk' not in args) or ('desk' in args and 'room' not in args):
            abort(422, message="Invalid Parameters, Desk and Room are mutually dependant and cannot be used individually")
        ## Check if the computer already exists
        doesComputerAlreadyExist = Computer.query.filter_by(mac_address=args['mac_address']).first()
        if doesComputerAlreadyExist is not None:
            abort(405, message='The supplied Computer already exists, please use a put request to update its values.')
        ## Parse the parameters into the data map for the Model creation
        machineData = {}
        machineData['mac_address'] = args['mac_address']
        machineData['ip_address'] = args['ip_address']
        machineData['machine_name'] = args['machine_name']
        machineData['os_name'] = args['os_name']
        machineData['os_release'] = args['os_release']
        machineData['os_build'] = args['os_build']
        ## Create our model
        machine = Computer(**machineData)
         ## If we need to link the computer to a desk
        if 'room' in args and 'desk' in args:
            ## Check if the room exists
            doesRoomExist = Room.query.filter_by(room_name=args['room']).first()
            if doesRoomExist is None:
                abort(404, message='Room not found')
            ## Check the desk exists
            doesDeskExist = Desk.query.filter_by(desk_id=args['desk']).join(Desk.room, aliased=True).filter_by(room_name=args['room']).first()
            if doesDeskExist is None:
                abort(404, message="Desk not found")
            else:
                ## As the desk exists, set the Foreign key to the index of the desk
                machine.desk_id = doesDeskExist.identifier
        db.session.add(machine)
        db.session.commit()
        ## Return that the resource has been created
        return "", 201

    ## The Put Verb Method
    @use_args(put_args)
    def put(self, args):
        ## Check the mutually inclusive optional parameters
        if ('room' in args and 'desk' not in args) or ('desk' in args and 'room' not in args):
            abort(422, message="Invalid Parameters, Desk and Room are mutually dependant and cannot be used individually")
        ## Check if the computer already exists
        computer = Computer.query.filter_by(mac_address=args['mac_address'])
        if computer.first() is None:
            abort(405, message='The supplied Computer does not exist, please create it via a POST request.')
        ## Parse the pushed args into a map of the data
        machineData = {}
        ## This is ugly, but each of these parameters are optional for the update, so we just check them one by one.
        machineData['mac_address'] = args['mac_address']
        if 'ip_address' in args:
            machineData['ip_address'] = args['ip_address']
        if 'machine_name' in args:
            machineData['machine_name'] = args['machine_name']
        if 'os_name' in args:
            machineData['os_name'] = args['os_name']
        if 'os_release' in args:
            machineData['os_release'] = args['os_release']
        if 'os_build' in args:
            machineData['os_build'] = args['os_build']
        ## Update the model
        computer.update(machineData)
        computer.first().updated_at = datetime.now()
        ## If we need to link the computer to a desk
        if 'room' in args and 'desk' in args:
            ## Check if the room exists
            doesRoomExist = Room.query.filter_by(room_name=args['room']).first()
            if doesRoomExist is None:
                abort(404, message='Room not found')
            ## Check the desk exists
            doesDeskExist = Desk.query.filter_by(desk_id=args['desk']).join(Desk.room, aliased=True).filter_by(room_name=args['room']).first()
            if doesDeskExist is None:
                abort(404, message="Desk not found")
            else:
                ## As the desk exists, set the Foreign key to the index of the desk
                computer.first().desk_id = doesDeskExist.identifier
        db.session.commit()
        ## Return that the resource has been updated
        return "", 202

    ## The Delete Verb Method
    @use_args(get_and_delete_args)
    def delete(self, args):
        ## Try and get the machine we want to delete
        machine = Computer.query.filter_by(identifier=args['id']).first()
        ## Check to see if the machine exists in the system
        if machine is None:
            abort(404, message='Computer not found')
        ## Delete the chosen Computer
        db.session.delete(machine)
        db.session.commit()
        ## Return 202 as the request was executed
        return "", 202
