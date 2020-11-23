from flask import request, jsonify

import ApiGateway.clients.bookings as bookings
import ApiGateway.clients.users as users
import ApiGateway.clients.notifications as notifications
import ApiGateway.clients.restaurants as restaurants

################ USERS ################################################


def get_users(ssn=None, phone=None, email=None, is_positive=None):
    return users.get_users(ssn=ssn,phone=phone,email=email,is_positive=is_positive)


def create_user():
    dict_user = request.json
    return users.create_user(dict_user)


def get_id_user(user_id):
    return users.get_user(user_id)


def edit_user(user_id):
    dict_user = request.json
    return users.edit_user(user_id,dict_user)


def delete_user(user_id):
    return users.delete_user(user_id)


def get_user_contacts(user_id, begin=None, end=None):
    return users.get_user_contacts(user_id, begin=begin, end=end)

################ BOOKINGS ################################################


def get_bookings(user=None, rest=None, table=None, begin=None, end=None, begin_entrance=None, end_entrance=None, with_user=False):
    if with_user:
        return get_bookings_with_user_data(user=user, rest=rest, table=table, begin=begin, end=end, begin_entrance=begin_entrance, end_entrance=end_entrance)
    return bookings.get_bookings(user=user, rest=rest, table=table, begin=begin, end=end, begin_entrance=begin_entrance, end_entrance=end_entrance)


def new_booking():
    req = request.json
    return bookings.new_booking(user_id=req["user_id"], rest_id=req["restaurant_id"], number_of_people=req["number_of_people"], booking_datetime=req["booking_datetime"])


def get_booking(booking_id, with_user=False):
    if with_user:
        return get_booking_with_user_data(booking_id=booking_id)
    return bookings.get_a_booking(booking_id)


def put_booking(booking_id, entrance=False):
    req = request.json
    if "number_of_people" not in req:
        req["number_of_people"] = None
    if "booking_datetime" not in req:
        req["booking_datetime"] = None
    return bookings.edit_booking(booking_id=booking_id, number_of_people=req["number_of_people"], booking_datetime=req["booking_datetime"], entrance=entrance)


def delete_booking(booking_id):
    return bookings.delete_booking(booking_id)


def get_booking_with_user_data(booking_id):
    booking, booking_status_code = bookings.get_a_booking(booking_id)
    if booking_status_code != 200:
        return booking, booking_status_code
    user,user_status_code = users.get_user(booking['user_id'])
    if user_status_code != 200:
        return user, user_status_code
    booking["user"] = user
    return booking, booking_status_code


def get_bookings_with_user_data(user=None, rest=None, table=None, begin=None, end=None, begin_entrance=None, end_entrance=None):
    bookings_list,bookings_status_code = bookings.get_bookings(user=user, rest=rest, table=table, begin=begin, end=end, begin_entrance=begin_entrance, end_entrance=end_entrance)
    if bookings_status_code != 200:
        return bookings_list,bookings_status_code
    for booking in bookings_list:
        user,user_status_code = users.get_user(booking['user_id'])
        if user_status_code != 200:
            return user,user_status_code
        booking["user"] = user

    return bookings_list, bookings_status_code

################ NOTIFICATIONS ################################################

def get_notifications(user_id, read=None):
    return notifications.get_notifications(user_id, read=read)

def new_notification(user_id):
    return notifications.create_notification(user_id, request.json)

def get_notification(notification_id):
    return notifications.get_notification(notification_id)

def edit_notification(notification_id):
    return notifications.edit_notification(notification_id, request.json)

################ RESTAURANTS ################################################

def get_restaurants(name=None, opening_time=None, open_day=None, cuisine_type=None, menu=None):
    return restaurants.get_restaurants(name, opening_time, open_day, cuisine_type, menu)

def post_restaurants():
    json = request.json
    return restaurants.post_restaurants(json)

def get_restaurant(restaurant_id):
    return restaurants.get_restaurant(restaurant_id)

def put_restaurant(restaurant_id):
    json = request.json
    return restaurants.put_restaurant(restaurant_id,json)

def delete_restaurant(restaurant_id):
    return restaurants.delete_restaurant(restaurant_id)

def get_restaurant_rating(restaurant_id):
    return restaurants.get_restaurant_rating(restaurant_id)

def post_restaurant_rating(restaurant_id):
    json = request.json
    return restaurants.post_restaurant_rating(restaurant_id,json)

################ TABLES ################################################

def get_restaurant_tables(restaurant_id,capacity=None):
    return restaurants.get_restaurant_tables(restaurant_id,capacity)

def post_restaurant_table(restaurant_id):
    json = request.json
    return restaurants.post_restaurant_table(restaurant_id,json)

def get_restaurant_table(restaurant_id, table_id):
    return restaurants.get_restaurant_table(restaurant_id,table_id)

def put_restaurant_table(restaurant_id, table_id):
    json = request.json
    return restaurants.put_restaurant_table(restaurant_id,table_id,json)

def delete_restaurant_table(restaurant_id, table_id):
    return restaurants.delete_restaurant_table(restaurant_id,table_id)