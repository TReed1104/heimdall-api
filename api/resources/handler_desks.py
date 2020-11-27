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

## Our resource for handling the creation, update and indexing of desks
class DeskHandler(Resource):
    get_and_delete_args = {
        'id': fields.Integer(required=True)
    }
    post_args = {
        'desk': fields.String(required=True),
        'room': fields.String(required=True)
    }
    put_args = {
        'id': fields.Integer(required=True),
        'new_room': fields.String(required=True)
    }

    @use_args(get_and_delete_args)
    def get(self, args):
        ## Get the desk
        desk = Desk.query.filter_by(identifier=args['id']).first()
        if desk is None:
            abort(404, message='Desk not found')
        ## Return the desks information
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "desk": desk.serialize
            }
        }
        return jsonify(response)

    @use_args(post_args)
    def post(self, args):
        ## Check if the room exists
        doesRoomExist = Room.query.filter_by(room_name=args['room']).first()
        if doesRoomExist is None:
            abort(404, message="Room not found")
        ## Check if the desk is already registered
        doesDeskExist = Desk.query.filter_by(desk_id=args['desk']).join(Desk.room, aliased=True).filter_by(room_name=args['room']).first()
        if doesDeskExist is not None:
            abort(405, message='The supplied desk already exists, please use a PUT request to update its data.')
        ## Parse the request body into a map
        deskData = {}
        deskData['desk_id'] = args['desk']
        ## Create the desk
        desk = Desk(**deskData)
        desk.room_id = Room.query.filter_by(room_name=args['room']).first().identifier
        db.session.add(desk)
        db.session.commit()
        return "", 201      ## Return that the resource has been created

    @use_args(put_args)
    def put(self, args):
        ## Check the desk exists
        desk = Desk.query.filter_by(identifier=args['id'])
        if desk.first() is None:
            abort(404, message="Desk does not exist")
        ## Check if the new room exists in the system
        newRoom = Room.query.filter_by(room_name=args['new_room']).first()
        if newRoom is None:
            abort(404, message="New Room does not exist")
        ## Check if the new room already has a desk of the new name
        doesDeskAlreadyExistInRoom = Desk.query.filter_by(desk_id=desk.first().desk_id).join(Desk.room, aliased=True).filter_by(room_name=args['new_room']).first()
        if doesDeskAlreadyExistInRoom is not None:
            abort(422, message='The new room already contains a desk of that name')
        ## Apply the update
        desk.first().room_id = newRoom.identifier
        desk.first().updated_at = datetime.now()
        db.session.commit()
        return "", 202      ## Return that the resource has been created

    @use_args(get_and_delete_args)
    def delete(self, args):
        ## Check if the desk exists in the system
        desk = Desk.query.filter_by(identifier=args['id']).first()
        if desk is None:
            abort(404, message='Desk not found')
        ## Delete the desk
        db.session.delete(desk)
        db.session.commit()
        return "", 202      ## Return 202 as the request was executed
