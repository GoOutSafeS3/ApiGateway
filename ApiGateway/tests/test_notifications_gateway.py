from datetime import date
import unittest 
import datetime

from ApiGateway.app import create_app 

class NotificationsTests(unittest.TestCase): 
    """ Tests Api Gateway interacting with other microservices """

    def setUp(self): 
        app = create_app()
        self.app = app.app 
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_create_notification(self):
        response = self.client.post("/notifications", json={
            "user_id": 1,
            "content": "test",
            "sent_on": datetime.datetime.now().isoformat()
        })
        self.assertEqual(response.status_code, 201)

        response = self.client.get(response.json["url"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['content'], "test")

        response = self.client.get("/notifications?user_id=1")
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["content"], "test")

    def test_read_notification(self):
        response = self.client.post("/notifications", json={
            "user_id": 1,
            "content": "test",
            "sent_on": datetime.datetime.today().isoformat()
        })
        self.assertEqual(response.status_code, 201)
        url = response.json["url"]

        response = self.client.patch(url, json={
            "read_on": datetime.datetime.now().isoformat()
        })
        self.assertEqual(response.status_code, 200)

    def test_notifications_read_date(self):
        response = self.client.get("/notifications", query_string={
            "user_id": 1,
            "read": "true"
        })
        self.assertEqual(response.status_code, 200)
        for noti in response.json:
            self.assertIsNotNone(noti["read_on"])
            
        response = self.client.get("/notifications", query_string={
            "user_id": 1,
            "read": "false"
        })
        self.assertEqual(response.status_code, 200)
        for noti in response.json:
            self.assertIsNone(noti["read_on"])