## Imports
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from models import computer, room, desk
from shared import db
from resources import list_computers, list_desks, list_rooms, list_availability
from resources import handler_computers, handler_desks, handler_rooms

## Create our Flask app and connect it to our database
app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('configs/main.cfg')
CORS(app)
db.init_app(app)
with app.app_context():
    db.create_all()

## Register the resources and the endpoints to access them
api.add_resource(list_computers.ComputerList, '/computers')
api.add_resource(list_desks.DeskList, '/desks')
api.add_resource(list_rooms.RoomList, '/rooms')
api.add_resource(list_availability.AvailabilityList, '/availability')
api.add_resource(handler_computers.ComputerHandler, '/computer_handler')
api.add_resource(handler_desks.DeskHandler, '/desk_handler')
api.add_resource(handler_rooms.RoomHandler, '/room_handler')

if __name__ == '__main__':
    ## Initialise the application, 0.0.0.0 means to use our machine ip and enable debugging if needed
    app.run(host='0.0.0.0', port='5000')
