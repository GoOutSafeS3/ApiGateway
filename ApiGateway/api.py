from flask import request, jsonify
from datetime import datetime, timedelta
from dateutil import parser

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
    old_user, status = users.get_user(user_id)
    
    if status != 200:
        return old_user, status
    
    result, status = users.edit_user(user_id, dict_user)

    if status != 200:
        return result, status

    if not old_user['is_positive'] and result['is_positive']:
        end = parser.parse(dict_user['positive_datetime'])
        begin = end - timedelta(days = 14)
        contacts, status = users.get_user_contacts(user_id, begin.isoformat(), end.isoformat())

        if status != 200:
            return contacts, status

        for contact in contacts:
            result, status = notifications.create_notification({
                "user_id": contact["id"],
                "content": "You have had contact with a Covid-19 positive in the last 14 days",
                "sent_on": datetime.now().isoformat()
            })
            if status != 200:
                return result, status

    return result, status


def delete_user(user_id):
    return users.delete_user(user_id)


def get_user_contacts(user_id, begin=None, end=None):
    return users.get_user_contacts(user_id, begin=begin, end=end)

################ BOOKINGS ################################################


def get_bookings(user=None, rest=None, table=None, begin=None, end=None, begin_entrance=None, end_entrance=None, with_user=False):
    """ Return the list of bookings.

    GET /bookings?[user=U_ID&][rest=R_ID&][table=T_ID&][begin=BEGING_DT&][end=END_DT&][begin_entrance=BEGING_ENT_DT&][end_entrance=END_ENT_DT&][with_user=true/false]

    It's possible to filter the bookings thanks the query's parameters.
    The parameters can be overlapped in any way.
    All paramters are optional.

    - user: All the booking of a specific user (by id)
    - rest: All the booking of a specific restaurant (by id)
    - table: All the booking of a specific table (by id)
    - begin: All bookings from a certain date onwards (datetime ISO 8601 - Chapter 5.6)
    - end: All bookings up to a certain date onwards (datetime ISO 8601 - Chapter 5.6)
    - begin_entrance: All bookings from a certain entrance date onwards (datetime ISO 8601 - Chapter 5.6)
    - end_entrance: All bookings up to a certain entrance date onwards (datetime ISO 8601 - Chapter 5.6)
    - with_user: If true adds at each bookings the user information

    If begin and not end is specified, all those starting from begin are taken. Same thing for end.

    Status Codes:
        200 - OK
        400 - Wrong datetime format
        500 - Error in communicating with the user service or problem with the database (try again)
    """
    if with_user:
        return get_bookings_with_user_data(user=user, rest=rest, table=table, begin=begin, end=end, begin_entrance=begin_entrance, end_entrance=end_entrance)
    return bookings.get_bookings(user=user, rest=rest, table=table, begin=begin, end=end, begin_entrance=begin_entrance, end_entrance=end_entrance)


def new_booking():
    """ Add a new booking.

    POST /bookings
    
    Returns the booking if it can be made, otherwise returns an error message.

    Requires a json object with:
        - number_of_people: the number of people for the booking
        - booking_datetime: the datetime of the booking
        - user_id: the id of the user who made the booking
        - restaurant_id: the id of the restaurant

    Status Codes:
        201 - The booking has been created
        400 - Wrong datetime
        409 - Impossible to change the booking (it is full, it is closed ...)
        500 - Error in communicating with the restaurant service or problem with the database (try again)
    """
    req = request.json
    return bookings.new_booking(user_id=req["user_id"], rest_id=req["restaurant_id"], number_of_people=req["number_of_people"], booking_datetime=req["booking_datetime"])


def get_booking(booking_id, with_user=False):
    """ Return a specific booking (request by id)

    GET /bookings/{booking_id}?[with_user=true/false]

    - with_user: [optional] If true adds the user information

    Status Codes:
        200 - OK
        404 - Booking not found
        500 - Error in communicating with the user service or problem with the database (try again)
    """
    if with_user:
        return get_booking_with_user_data(booking_id=booking_id)
    return bookings.get_a_booking(booking_id)


def put_booking(booking_id, entrance=False):
    """ Edit a booking.

    GET /bookings/{booking_id}?[entrance=true/false]

    Changes the number of people and/or the date of the booking. 
    Or marks the user's entry.

    The request to mark the entrance is made through the query parameter entrance (a boolean)

    Change requests are made through json objects with the following properties (both optional)
        - booking_datetime: the new requested datetime
        - number_of_people: the new requested number of people

    If one of the two fields is not set, the one already entered is recovered.
    If both are not entered the request is void (unless required to mark the entry()in this case the json is ignored).

    If entry is marked, other requests for changes are ignored (if the user has already entered the changes no longer make sense).
    Likewise, if the entry is marked, no more changes can be made.

    The booking must not have already passed, in the event of a change.

    Change of a booking may not always be possible (on the requested date there are no seats available, the restaurant is closed on that date ...)

    Status Codes:
        200 - OK
        400 - Wrong datetime or bad request (entry already marked)
        404 - Booking not found
        409 - Impossible to change the booking
        500 - Error in communicating with the restaurant service or problem with the database (try again)
        """

    req = request.json
    if "number_of_people" not in req:
        req["number_of_people"] = None
    if "booking_datetime" not in req:
        req["booking_datetime"] = None
    return bookings.edit_booking(booking_id=booking_id, number_of_people=req["number_of_people"], booking_datetime=req["booking_datetime"], entrance=entrance)


def delete_booking(booking_id):
    """ Delete a booking specified by the id.

    DELETE /bookings/{booking_id}
    
    Deletion is only possible if the booking has not yet passed.

    Otherwise it remains stored (necessary for contact tracing)

    Status Codes:
        204 - Deleted
        404 - Booking not found
        403 - The booking cannot be deleted: it is a past reservation
        500 - Error with the database
    """
    return bookings.delete_booking(booking_id)


def get_booking_with_user_data(booking_id):
    """ Return a specific booking with user data.

    Status Codes:
        200 - OK
        404 - Booking not found
        500 - Error in communicating with the user service or problem with the database (try again)
    """
    booking, booking_status_code = bookings.get_a_booking(booking_id)
    if booking_status_code != 200:
        return booking, booking_status_code
    user,user_status_code = users.get_user(booking['user_id'])
    if user_status_code != 200:
        return user, user_status_code
    booking["user"] = user
    return booking, booking_status_code


def get_bookings_with_user_data(user=None, rest=None, table=None, begin=None, end=None, begin_entrance=None, end_entrance=None):
    """ Return the list of bookings with user data.

    It's possible to filter the bookings thanks the query's parameters.
    The parameters can be overlapped in any way.
    All paramters are optional.

    - user: All the booking of a specific user (by id)
    - rest: All the booking of a specific restaurant (by id)
    - table: All the booking of a specific table (by id)
    - begin: All bookings from a certain date onwards (datetime ISO 8601 - Chapter 5.6)
    - end: All bookings up to a certain date onwards (datetime ISO 8601 - Chapter 5.6)
    - begin_entrance: All bookings from a certain entrance date onwards (datetime ISO 8601 - Chapter 5.6)
    - end_entrance: All bookings up to a certain entrance date onwards (datetime ISO 8601 - Chapter 5.6)

    If begin and not end is specified, all those starting from begin are taken. Same thing for end.

    Status Codes:
        200 - OK
        400 - Wrong datetime format
        500 - Error in communicating with the user service or problem with the database (try again)
    """
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

def new_notification():
    return notifications.create_notification(request.json)

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