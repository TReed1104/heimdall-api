from datetime import datetime
from shared import db

## SQLAlchemy model for a Room
class Room(db.Model):
    __tablename__ = 'heimdall_rooms'
    identifier = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(255), unique=False, nullable=False)
    subnets = db.Column(db.String(255), unique=False, nullable=False)
    capacity = db.Column(db.Integer, unique=False, nullable=False, default=0)
    has_availability_map = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    desks = db.relationship('Desk', back_populates='room')  ## Link the Room to the desks
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, **kwargs):
        ## Default constructor handling by SQLAlchemy ORM
        super(Room, self).__init__(**kwargs)

        ## Custom constructor code
        self.validateSubnets()

    @property
    def serialize(self):
        return {
            'id': self.identifier,
            'name': self.room_name,
            'subnets': self.subnets,
            'capacity': self.capacity,
            'number_of_desks': len(self.desks),
            'number_of_computers': self.computer_count,
            'has_availability_map': self.has_availability_map
        }
    
    @property
    def computer_count(self):
        ## Check the Room has desks
        if self.desks is None:
            return 0
        ## Count the computers
        computerCount = 0
        for desk in self.desks:
            if desk.computers is not None:
                computerCount += len(desk.computers)
        return computerCount

    def validateSubnets(self):
        ## Check the subnet is a valid format
        suppliedSubnets = self.subnets.split(',')  ## Split into each of the supplied subnets
        for subnet in suppliedSubnets:
            subnetSections = subnet.split('.')
            ## Check the subnet was composed of 3 sections, e.g. 192.168.0. Subnets with trailing '.' will also be marked as invalid
            if len(subnetSections) != 3:
                self.subnets = "Invalid"
            for section in subnetSections:
                ## check the subnet section is not longer than 3 characters
                if len(section) > 3:
                    self.subnets = "Invalid"
