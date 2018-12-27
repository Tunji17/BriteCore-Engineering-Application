import os
import json
import unittest
from datetime import date

from main_app import app, db, models
from main_app.models import User, Client, Request, ProductEnum
from config.settings import basedir

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
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['DEBUG'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.appd = app.test_client()
        self.client = self.app.test_client
        self.request = {
                        'title': 'title 1',
                        'description': "description 2",
                        'client': 1,
                        'priority': 1,
                        'target_date': '2018-11-06',
                        'product': 'claims'
                    }

        db.create_all()



        ########################
        #### helper methods ####
        ########################

    def register(self, username, email, password, confirm):
        return self.appd.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.appd.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def create_client_and_request(self):
        client = Client(name="client A")
        data = [Request(
            title=f'title {index+1}',
            description=f'description {index+1}',
            client_id=1,
            priority=index+1,
            target_date=date(2018,11,6),
            product=product
         ) for index, product in enumerate(ProductEnum)]
        data.append(client)
        db.session.add_all(data)
        db.session.commit()

        ###############
        #### tests ####
        ###############

    def test_main_page(self):
        response = self.appd.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)



    def test_valid_user_registration(self):
        response = self.register('johndoe','johndoe@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_registration_different_passwords(self):
        response = self.register('johndoe','johndoe@gmail.com', 'FlaskIsAwesome', 'FlaskIsNotAwesome')
        #self.assertNotEqual(response.status_code, 200)
        self.assertIn(b'Passwords must match', response.data)


    def test_valid_login(self):
        response = self.login('johndoe@gmail.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_with_wrong_password(self):
        response = self.login('johndoe@gmail.com','FlaskIsNotAwesome')
        #self.assertNotEqual(response.status_code, 200)
        self.assertIn(b'Password', response.data)

    def test_request_creation(self):
        res = self.client().post('/Requests', data=self.request)
        self.assertEqual(Request.query.count(), 1)
        self.assertEqual(res.status_code, 302)

    def test_requests_are_reordered_when_priority_on_new_request_is_already_set(self):
        self.create_client_and_request()
        self.assertEqual(Request.query.count(), 4)
        self.assertEqual(Request.query.get(1).title, 'title 1')
        self.assertEqual(Request.query.get(1).priority, 1)
        res = self.client().post('/Requests', data=self.request)
        self.assertEqual(Request.query.get(1).priority, 2)
        self.assertEqual(Request.query.get(2).priority, 3)
        self.assertEqual(Request.query.get(3).priority, 4)
        self.assertEqual(Request.query.get(4).priority, 5)
        self.assertEqual(Request.query.get(5).priority, 1)
        self.assertEqual(Request.query.count(), 5)
        self.request.update(priority=3)
        res = self.client().post('/Requests', data=self.request)
        self.assertEqual(Request.query.get(6).priority, 3)
        self.assertEqual(Request.query.get(2).priority, 4)
        self.assertEqual(Request.query.get(3).priority, 5)
        self.assertEqual(Request.query.count(), 6)
        self.assertEqual(res.status_code, 302)

    def test_no_duplicate_if_priority_on_new_request_is_equal_to_all_request_count(self):
        self.create_client_and_request()
        self.assertEqual(Request.query.count(), 4)
        self.assertEqual(Request.query.get(1).title, 'title 1')
        self.assertEqual(Request.query.get(1).priority, 1)
        self.request.update({'priority':4})
        res = self.client().post('/Requests', data=self.request)
        self.assertEqual(Request.query.get(1).priority, 1)
        self.assertEqual(Request.query.get(2).priority, 2)
        self.assertEqual(Request.query.get(3).priority, 3)
        self.assertEqual(Request.query.get(4).priority, 5)
        self.assertEqual(Request.query.get(5).priority, 4)
        self.assertEqual(Request.query.count(), 5)

    def test_requests_does_not_get_reordered_if_priority_on_new_request_is_not_set(self):
        self.create_client_and_request()
        self.assertEqual(Request.query.count(), 4)
        self.assertEqual(Request.query.get(1).title, 'title 1')
        self.assertEqual(Request.query.get(1).priority, 1)
        self.request.update(priority=5)
        res = self.client().post('/Requests', data=self.request)
        self.assertEqual(Request.query.get(1).priority, 1)
        self.assertEqual(Request.query.get(2).priority, 2)
        self.assertEqual(Request.query.get(3).priority, 3)
        self.assertEqual(Request.query.get(4).priority, 4)
        self.assertEqual(Request.query.get(5).priority, 5)
        self.assertEqual(Request.query.count(), 5)
        self.assertEqual(res.status_code, 302)

        # teardown initialize variables
    def tearDown(self):
        db.session.remove()
        db.drop_all()
