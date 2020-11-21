from os import SEEK_CUR
import unittest 
import datetime

from ApiGateway.app import create_app 


class BookingsTests(unittest.TestCase): 
    """ Tests Api Gateway interacting with other microservices """

############################ 
#### setup and teardown #### 
############################ 

    # executed prior to each test 
    def setUp(self): 
        app = create_app()
        self.app = app.app 
        self.app.config['TESTING'] = True 

    # executed after each test 
    def tearDown(self): 
        pass 

###############
#### tests #### 
############### 

    
    def test_get_bookings(self):
        client = self.app.test_client()
        response = client.get('/bookings')
        js = response.get_json()
        self.assertEqual(response.status_code,200,msg=js)
        self.assertEqual(len(js),6,msg=js)

    def test_get_booking(self):
        client = self.app.test_client()
        response = client.get('/bookings/1')
        js = response.get_json()
        self.assertEqual(response.status_code,200,msg=js)
        self.assertEqual(js["id"],1,msg=js)

    def test_get_bookings_with_users(self):
        client = self.app.test_client()
        response = client.get('/bookings?with_user=true')
        js = response.get_json()
        self.assertEqual(response.status_code,200,msg=js)
        self.assertEqual(len(js),6,msg=js)
        for b in js:
            self.assertEqual(b["user_id"],b["user"]["id"],msg=b)

    def test_get_booking_with_user(self):
        client = self.app.test_client()
        response = client.get('/bookings/1?with_user=true')
        js = response.get_json()
        self.assertEqual(response.status_code,200,msg=js)
        self.assertEqual(js["id"],1,msg=js)
        self.assertEqual(js["user_id"],js["user"]["id"],msg=js)

    """
    def test_delete_booking(self):
        # Need to create a new booking first
        client = self.app.test_client()
        response = client.delete('/bookings/1')
        js = response.get_json()
        self.assertEqual(response.status_code,204,msg=js)
        
        response = client.get('/bookings/1')
        js = response.get_json()
        self.assertEqual(response.status_code,404,msg=js)
    
    """