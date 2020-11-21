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
        self.assertEquals(len(js),0,msg=js)