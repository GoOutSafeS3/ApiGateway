from datetime import date
from os import SEEK_CUR
import unittest 
import datetime

from ApiGateway.app import create_app 

restaurant_add = {
    "url": "/restaurants/5",
    "id": 5,
    "name": "Rest 5",
    "rating_val": 0.0,
    "rating_num": 0,
    "lat": 42.41,
    "lon": 42.41,
    "phone": "050123456",
    "first_opening_hour": 2,
    "first_closing_hour": 5,
    "second_opening_hour": 15,
    "second_closing_hour": 20,
    "occupation_time": 1,
    "cuisine_type": "cuisine_type",
    "menu": "menu",
    "closed_days": [1,2,3,4,5,6,7]
}

restaurant_put = {
    "url": "/restaurants/5",
    "id": 5,
    "name": "Rest 5 new",
    "rating_val": 0.0,
    "rating_num": 0,
    "lat": 42.41,
    "lon": 42.41,
    "phone": "050123456",
    "first_opening_hour": 2,
    "first_closing_hour": 6,
    "second_opening_hour": 15,
    "second_closing_hour": 20,
    "occupation_time": 1,
    "cuisine_type": "cuisine_type",
    "menu": "menu",
    "closed_days": [1,2,3,4,5,6,7]
}

restaurant_post_keys= [
    "name",
    "lat",
    "lon",
    "phone",
    "first_opening_hour",
    "first_closing_hour",
    "second_opening_hour",
    "second_closing_hour",
    "occupation_time",
    "cuisine_type",
    "menu",
    "closed_days",
]

table_post_keys= [
    "capacity",
]

table_add = {"url": "/restaurants/5/tables/7", "id":7, "restaurant_id": 5, "capacity":2}
table_edit ={"url": "/restaurants/5/tables/7", "id":7, "restaurant_id": 5, "capacity":5}

def clone_for_post(obj,keys):
    dup = {}
    for k,v in obj.items():
        if k in keys:
            dup[k] = v
    return dup

def same_restaurant(rest,rest2):
    for k in rest.keys():
        if rest[k] != rest2[k]:
            return str(rest[k])+"\n"+k+"\n"+str(rest2[k])
    return None

class RestaurantsTests(unittest.TestCase): 
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

    
    def test_01_get_restaurants(self):
        client = self.app.test_client()
        response = client.get('/restaurants?name=Rest&opening_time=11&open_day=2&cuisine_type=cuisine&menu=menu')
        json = response.get_json()
        self.assertEqual(response.status_code,200,msg=json)
        self.assertEqual(len(json),2,msg=json)

    def test_02_post_restaurants(self):
        client = self.app.test_client()
        r = clone_for_post(restaurant_add,restaurant_post_keys)
        response = client.post('/restaurants', json=r)
        json = response.get_json()
        self.assertEqual(response.status_code,201,msg=json)
        self.assertIsNone(same_restaurant(json,restaurant_add),msg="\n"+str(json)+"\n\n"+str(restaurant_add))

    def test_03_get_restaurant(self):
        client = self.app.test_client()
        response = client.get(restaurant_add["url"])
        json = response.get_json()
        self.assertEqual(response.status_code,200,msg=json)
        self.assertIsNone(same_restaurant(json,restaurant_add),msg="\n"+str(json)+"\n\n"+str(restaurant_add))

    def test_04_put_restaurant(self):
        client = self.app.test_client()
        r = clone_for_post(restaurant_put,restaurant_post_keys)
        response = client.put(restaurant_put["url"], json=r)
        json = response.get_json()
        self.assertEqual(response.status_code,200,msg=json)
        self.assertIsNone(same_restaurant(json,restaurant_put),msg="\n"+str(json)+"\n\n"+str(restaurant_put))

    def test_12_delete_restaurant(self):
        client = self.app.test_client()
        response = client.delete(restaurant_add["url"])
        self.assertEqual(response.status_code,204,msg=response.get_data())

    def test_05_get_restaurant_rate(self):
        client = self.app.test_client()
        response = client.get("/restaurants/%d/rate"%restaurant_add["id"])
        json = response.get_json()
        self.assertEqual(response.status_code,200,msg=json)
        self.assertEqual(json["rating"], restaurant_add["rating_val"], msg =json)
        self.assertEqual(json["ratings"], restaurant_add["rating_num"], msg =json)

    def test_06_post_restaurant_rate(self):
        client = self.app.test_client()
        r = restaurant_add
        rating_add = {"rater_id": 1, "rating": 3}
        response = client.post("%s/rate" % r["url"], json=rating_add)
        self.assertEqual(response.status_code, 202, msg=response.get_data())

    def test_07_get_restaurant_tables(self):
        client = self.app.test_client()
        response = client.get('/restaurants/3/tables?capacity=3')
        json = response.get_json()
        self.assertEqual(response.status_code,200,msg=json)
        self.assertEqual(len(json),2,msg=json)

    def test_08_post_restaurant_tables(self):
        client = self.app.test_client()
        t = clone_for_post(table_add, table_post_keys)
        response = client.post('/restaurants/%d/tables'%table_add["restaurant_id"], json=t)
        json = response.get_json()
        self.assertEqual(response.status_code,201,msg=json)
        self.assertEqual(json,table_add,msg=json)

    def test_09_get_restaurant_table(self):
        client = self.app.test_client()
        response = client.get(table_add["url"])
        json = response.get_json()
        self.assertEqual(response.status_code,200,msg=json)
        self.assertEqual(json,table_add,msg=json)

    def test_10_put_restaurant_table(self):
        client = self.app.test_client()
        t = clone_for_post(table_edit, table_post_keys)
        response = client.put("%s"%table_edit["url"], json=t)
        json = response.get_json()
        self.assertEqual(response.status_code,200,msg=json)
        self.assertEqual(json,table_edit,msg=json)

    def test_11_delete_restaurant_table(self):
        client = self.app.test_client()
        response = client.delete(table_add["url"])
        self.assertEqual(response.status_code,204,msg=response.get_data())

