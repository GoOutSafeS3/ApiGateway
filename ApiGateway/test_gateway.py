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

    def test_post_edit_delete_booking(self):
        client = self.app.test_client()

        booking = {
            "user_id":1,
            "restaurant_id":3,
            "number_of_people":3, 
            "booking_datetime": (datetime.datetime.now().replace(hour=13) + datetime.timedelta(days=1)).isoformat()
            }
        response = client.post('/bookings',json=booking)
        js = response.get_json()
        self.assertEqual(response.status_code, 201, msg=js) # good request: created

        response = client.post('/bookings',json=booking) # same booking again
        self.assertEqual(response.status_code, 409, msg=response.get_json()) # no free tables (now) 'cause too much people (no free tables with such capacity)

        new_time = (datetime.datetime.now().replace(hour=13,minute=30) + datetime.timedelta(days=1)).isoformat()

        booking = {
            "number_of_people":2, 
            "booking_datetime": new_time
            }

        response = client.put('/bookings/'+str(js["id"]),json=booking)
        js1 = response.get_json()
        self.assertEqual(response.status_code,200,msg=js1)
        self.assertEqual(js["id"],js1["id"],msg=js1)
        self.assertEqual(js1["number_of_people"],2,msg=js)
        self.assertEqual(js1["booking_datetime"],new_time+"Z",msg=js)

        client = self.app.test_client()
        response = client.delete('/bookings/'+str(js["id"]))
        self.assertEqual(response.status_code,204,msg="url="+'/bookings/'+str(js["id"]))
        
        response = client.get('/bookings/'+str(js["id"]))
        self.assertEqual(response.status_code,404,msg="url="+'/bookings/'+str(js["id"])+"\n"+response.get_data(as_text=True))