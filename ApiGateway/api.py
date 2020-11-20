from flask import request, jsonify
from errors import Error500, Error404, Error400

################ USERS ################################################

def get_users(ssn=None, phone=None, email=None, is_positive=None):
    pass

def create_user():
    pass

def get_id_user(user_id):
    pass

def edit_user(user_id):
    pass

def delete_user(user_id):
    pass

def get_user_contacts(user_id, begin=None, end=None):
    pass

################ BOOKINGS ################################################

def get_bookings(user=None, rest=None, table=None, begin=None, end=None, begin_entrance=None, end_entrance=None):
    pass

def new_booking():
    pass

def get_booking(booking_id):
    pass

def put_booking(booking_id, entrance=False):
    pass

def delete_booking(booking_id):
    pass

def get_notifications(**kwargs):
    pass

def new_notification(body):
    pass

def get_notification(notification_id):
    pass

def edit_notification(notification_id, body):
    pass

def get_restaurants(name=None, opening_time=None, open_day=None, cuisine_type=None, menu=None):
    pass

def post_restaurants():
    pass

def get_restaurant(restaurant_id):
    pass

def put_restaurant(restaurant_id):
    pass

def delete_restaurant(restaurant_id):
    pass

def get_restaurant_rating(restaurant_id):
    pass

def post_restaurant_rating(restaurant_id):
    pass

def get_restaurant_tables(restaurant_id):
    pass

def post_restaurant_table(restaurant_id):
    pass

def get_restaurant_table(restaurant_id, table_id):
    pass

def put_restaurant_table(restaurant_id, table_id):
    pass

def delete_restaurant_table(restaurant_id, table_id):
    pass