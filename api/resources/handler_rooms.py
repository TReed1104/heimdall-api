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

class RoomHandler(Resource):
    get_and_delete_args = {
        'id': fields.Integer(required=True)
    }
    post_args = {
        'room': fields.String(required=True),
        'subnets': fields.String(required=True),
        'capacity': fields.Integer(required=True),
        'has_availability_map': fields.Bool(required=True)
    }
    put_args = {
        'id': fields.Integer(required=True),
        'subnets': fields.String(),
        'capacity': fields.Integer(),
        'has_availability_map': fields.Bool()
    }

    @use_args(get_and_delete_args)
    def get(self, args):
        ## Find the Room
        room = Room.query.filter_by(identifier=args['id']).first()
        ## No machines found, abort the request
        if room is None:
            abort(404, message="Room not found")
        ## We've found the Room, serialise it into a json format for the response
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "room": room.serialize
            }
        }
        return jsonify(response)

    @use_args(post_args)
    def post(self, args):
        ## Check if the room is already registered
        doesRoomExist = Room.query.filter_by(room_name=args['room']).first()
        if doesRoomExist is not None:
            abort(405, message='The supplied room already exists, please use a put request to update its values.')
        ## Create the dicitonary of our passed values
        roomData = {}
        roomData['room_name'] = args['room']
        roomData['subnets'] = args['subnets']
        roomData['capacity'] = args['capacity']
        roomData['has_availability_map'] = args['has_availability_map']
        ## The room doesn't exist, create it
        room = Room(**roomData)
        if room.subnets == 'Invalid':
            abort(422, message='Invalid Subnet')
        db.session.add(room)
        db.session.commit()
        return "", 201

    @use_args(put_args)
    def put(self, args):
        ## Check if the room is already registered
        doesRoomExist = Room.query.filter_by(identifier=args['id'])
        if doesRoomExist.first() is None:
            abort(405, message='The supplied room does not exist, please create it via a POST request.')
        ## Create the dicitonary of our passed values
        roomData = {}
        ## As the params are optional, check what ones are present
        if 'subnets' in args:
            roomData['subnets'] = args['subnets']
        if 'capacity' in args:
            roomData['capacity'] = args['capacity']
        if 'has_availability_map' in args:
            roomData['has_availability_map'] = args['has_availability_map']
        ## The room exists, update it
        doesRoomExist.update(roomData)
        doesRoomExist.first().updated_at = datetime.now()
        ## If the a new subnet has been pushed, validate it
        if 'subnets' in args:
            ## Validate that the update didn't include a bad subnet
            doesRoomExist.first().validateSubnets()
            if doesRoomExist.first().subnets == 'Invalid':
                abort(422, message='Invalid Subnet')
        db.session.commit()
        return "", 202

    @use_args(get_and_delete_args)
    def delete(self, args):
        ## Find the Room
        roomToDelete = Room.query.filter_by(identifier=args['id']).first()
        if roomToDelete is None:
            abort(404, message="Room not found")
        ## Find and delete each desk registered to room we are deleting
        desksToDelete = Desk.query.join(Desk.room, aliased=True).filter_by(room_name=roomToDelete.room_name).all()
        if desksToDelete is not None:
            for desk in desksToDelete:
                db.session.delete(desk)
        ## Delete the room
        db.session.delete(roomToDelete)
        db.session.commit()
        ## Return 202 as the request was executed
        return "", 202
