from ApiGateway.app import create_app
import unittest
import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class UsersTest(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.app
        self.app.config['TESTING'] = True

    def tearDown(self):
        pass

    def test_get_users(self):
        client = self.app.test_client()
        response = client.get('/users')
        response_json = response.get_json()
        self.assertEqual(response.status_code, 200, msg=response_json)

    def test_get_positive_users(self):
        client = self.app.test_client()
        response = client.get('/users?is_positive=True')
        resp_json = response.get_json()
        self.assertEqual(response.status_code, 200, msg=resp_json)
        user = client.get('users/13')
        user_json = user.get_json()
        self.assertDictEqual(resp_json[0], user_json)

    def test_get_negative_users(self):
        client = self.app.test_client()
        response = client.get('/users?is_positive=False')
        resp_json = response.get_json()
        self.assertEqual(response.status_code, 200, msg=resp_json)

    def test_get_user(self):
        client = self.app.test_client()
        response = client.get('/users/1')
        user_1 = {
          "email": "gianni@example.com",
          "firstname": "Gianni",
          "id": 1,
          "is_active": True,
          "is_admin": False,
          "is_anonymous": False,
          "is_health_authority": False,
          "is_operator": False,
          "is_positive": False,
          "lastname": "Barbuti",
          "phone": "46966711",
          "positive_datetime": None,
          "ssn": None
        }
        self.assertDictContainsSubset(user_1,response.get_json())

    def test_create_user(self):
        client = self.app.test_client()
        user_new = {
            "email": "eleonora@example.com",
            "firstname": "Eleonora",
            'password':'eleonora',
            "is_admin": False,
            "is_health_authority": False,
            "is_operator": False,
            "is_positive": False,
            "lastname": "Corridori",
            "phone": "4342517754",
            "dateofbirth": datetime.datetime.today()- datetime.timedelta(weeks=1400,days=21),
            "ssn": 'LNRCRRDR34H54H78'
        }
        response = client.post('/users', json=user_new)
        self.assertEqual(response.status_code, 200)
        response = client.get('/users?email=eleonora@example.com')
        self.assertEqual(response.status_code, 200)

    def test_edit_user(self):
        client = self.app.test_client()
        user_modify = {
            "email": "daniele@example.com",
            "firstname": "Daniele",
            'password': generate_password_hash('daniele'),
            "is_admin": False,
            "is_health_authority": False,
            "is_operator": False,
            "is_positive": False,
            "lastname": "Corridori",
            "phone": "0934523345",
            "dateofbirth": datetime.datetime.today() - datetime.timedelta(weeks=1400, days=21),
            "ssn": 'LNRCRRDR34H54H78'
        }
        response = client.put('users/2',json=user_modify)
        self.assertEqual(response.status_code, 200)

    def test_user_contacts(self):
        client = self.app.test_client()
        response = client.get('users/2/contacts')
        user = client.get('users/3')
        self.assertEqual(response.status_code, 200)

    def test_new_user(self):
        client = self.app.test_client()
        user_new = {
            "email": "laura@example.com",
            "firstname": "Laura",
            'password': 'laura',
            "is_admin": False,
            "is_health_authority": False,
            "is_operator": False,
            "is_positive": False,
            "lastname": "Benni",
            "phone": "4696124",
            "dateofbirth": datetime.datetime.today() - datetime.timedelta(weeks=1400, days=21)
        }
        response = client.post('/users', json=user_new)
        self.assertEqual(response.status_code, 200)
        response = client.get('/users?email=laura@example.com')
        self.assertEqual(response.status_code, 200)