from datetime import datetime
from shared import db

## SQLAlchemy model for a Computer
class Computer(db.Model):
    __tablename__ = 'heimdall_computers'     ## the name of the table to be generated by SQLalchemy
    identifier = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(255), unique=False, nullable=False)
    mac_address = db.Column(db.String(255), unique=False, nullable=False)
    ip_address = db.Column(db.String(255), unique=False, nullable=False)
    os_name = db.Column(db.String(255), unique=False, nullable=False)
    os_release = db.Column(db.String(255), unique=False, nullable=False)
    os_build = db.Column(db.String(255), unique=False, nullable=False)
    status = db.Column(db.String(255), nullable=False, default="Good")
    desk_id = db.Column(db.Integer, db.ForeignKey("heimdall_desks.identifier"))      ## Foreign key to the desk
    desk = db.relationship('Desk', back_populates="computers")              ## Link many computers to one desk (many-to-1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    ## Serialise the object to being a json object
    @property
    def serialize(self):
        return {
            'id': self.identifier,
            'machine_name': self.machine_name,
            'mac_address': self.mac_address,
            'ip_address': self.ip_address,
            'os_name': self.operating_system,
            'os_release': self.os_release,
            'os_build': self.os_build,
            'status': self.status,
            'desk': self.desk_number,
            'desk_id': self.desk_id,
            'room': self.room_name,
            'room_id': self.room_id,
            'updated_at': self.updated_at
        }
    @property
    def trimmed_serialize(self):
        return {
            'id': self.identifier,
            'machine_name': self.machine_name,
            'mac_address': self.mac_address,
            'os_name': self.operating_system,
            'status': self.status,
            'desk': self.desk_number,
            'desk_id': self.desk_id,
            'room': self.room_name,
            'room_id': self.room_id,
            'updated_at': self.updated_at
        }

    ## Model funciton for updating the machines operational status
    def updateStatus(self, now):
        statusTypes = ['On', 'Asleep', 'Off', 'Check PC']   ## Define the valid status types
        timeDelta = abs(self.updated_at - now)
        stateIndex = 0
        if timeDelta.days < 1:
            ## If its been over 6 minutes, set the status to sleeping as the machine has missed its call home timer
            if (timeDelta.seconds / 60) > 6:
                stateIndex = 1
        ## Over a day, set the status to Off
        if timeDelta.days >= 1:
            stateIndex = 2
        ## Over 5 days, set status to Check PC
        if timeDelta.days >= 5:
            stateIndex = 3
        self.status = statusTypes[stateIndex]

    ## Model function for checking availability
    def checkAvailability(self):
        ## Update the PCs operational status
        self.updateStatus(datetime.now())
        ## Check the PC is marked as working
        if self.status == "Check PC":
            return 'Broken'
        ## Check if PC has been seen recently
        if self.status == "On":
            return 'Not Available'
        ## As the PC is not marked to check and isn't "on", say its available
        return 'Available'

    ## Model function for getting the desks position
    @property
    def desk_number(self):
        ## Position generation
        if self.desk is not None:
            return self.desk.desk_id
        else:
            return "Not Set"

    ## Model function for getting its room number
    @property
    def room_name(self):
        if self.desk is not None:
            if self.desk.room is not None:
                return self.desk.room.room_name
        return "Not Set"

    @property
    def room_id(self):
        if self.desk is not None:
            if self.desk.room is not None:
                return self.desk.room.identifier
        return "Not Set"

    @property
    def operating_system(self):
        if self.os_name == 'Darwin':
            return 'MacOS'
        else:
            return self.os_name
