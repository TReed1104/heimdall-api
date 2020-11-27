from datetime import datetime
from shared import db

## An example of a SQLAlchemy model
class ExampleModel(db.Model):
    __tablename__ = 'example_models'
    identifier = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def serialize(self):
        return {
            'id': self.identifier
        }
