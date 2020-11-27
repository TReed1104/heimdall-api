from datetime import datetime
from shared import db

## SQLAlchemy model for a Desk
class Desk(db.Model):
    __tablename__ = 'heimdall_desks'
    identifier = db.Column(db.Integer, primary_key=True)
    desk_id = db.Column(db.String(255), unique=False, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("heimdall_rooms.identifier"))      ## Foreign Key to the room
    room = db.relationship('Room', back_populates="desks")                  ## Link to a Room (many-to-1)
    computers = db.relationship('Computer', back_populates='desk')          ## Link to a desk to multiple computers (1-to-many)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def serialize(self):
        return {
            'id': self.identifier,
            'name': self.desk_id,
            'room': self.get_room,
            'room_id': self.room_id,
            'number_of_computers': len(self.computers),
            'computers': self.get_computers
        }

    @property
    def get_room(self):
        if self.room is not None:
            return self.room.room_name
        return "Not Set"

    @property
    def get_computers(self):
        if self.computers is None:
            return []
        else:
            computers = []
            for computer in self.computers:
                computers.append(computer.trimmed_serialize)
            return computers
