import os
import json
import unittest
from datetime import date

from main_app import app, db, models
from main_app.models import User, Client, Request, ProductEnum
from main_app import basedir

TEST_DB = 'test.db'
class Test_main_app(unittest.TestCase):
    """
    this class is for testing the main_app
    """
    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        pass


        ###############
        #### tests ####
        ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        ########################
        #### helper methods ####
        ########################

    def register(self, username, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_valid_user_registration(self):
        response = self.register('johndoe','johndoe@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)


    def test_valid_login(self):
        response = self.login('johndoe@gmail.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)

    def
