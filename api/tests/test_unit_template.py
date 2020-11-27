import json
import unittest
from shared import db
from main import app

class UnitTest_Template(unittest.TestCase):
    ## Setup Functions
    def setUp(self):
        app.config.from_pyfile('configs/testing.cfg')
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    ## Teardown
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
