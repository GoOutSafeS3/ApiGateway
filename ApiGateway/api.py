from flask import request, jsonify

import ApiGateway.clients.bookings as bookings
import ApiGateway.clients.users as users

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

def get_notifications(**kwargs):
    pass

def new_notification(body):
    pass

def get_notification(notification_id):
    pass

def edit_notification(notification_id, body):
    pass

################ RESTAURANTS ################################################

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

################ TABLES ################################################

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