from flask_testing import TestCase
from VicSM import create_app, db


class MyTest(TestCase):

    def create_app(self):
        # pass in test configuration
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True

        return app

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
