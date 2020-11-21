import datetime

from ApiGateway.clients.utils import _get, _post, _put, _delete

BOOKINGS_SERVICE = "http://bookings:8080/"


def get_bookings(user=None, rest=None, table=None, begin=None, end=None, begin_entrance=None, end_entrance=None):
    url = BOOKINGS_SERVICE+"bookings?"

    if user is not None:
        url += "user="+str(user)+"&"

    if rest is not None:
        url += "rest="+str(rest)+"&"

    if table is not None:
        url += "table="+str(table)+"&"

    if begin is not None:
        url += "begin="+str(begin)+"&"

    if end is not None:
        url += "end="+str(end)+"&"

    if begin_entrance is not None:
        url += "begin_entrance="+str(begin_entrance)+"&"

    if end_entrance is not None:
        url += "end_entrance="+str(end_entrance)+"&"

    return _get(url)

def get_a_booking(id):
    return _get(BOOKINGS_SERVICE+"bookings/"+str(id))

def new_booking(user_id, rest_id, number_of_people, booking_datetime):
    booking = {
        "user_id":user_id,
        "restaurant_id":rest_id,
        "number_of_people":number_of_people,
        "booking_datetime":booking_datetime,
    }

    return _post(BOOKINGS_SERVICE+"bookings",booking)

def edit_booking(booking_id, number_of_people=None, booking_datetime=None, entrance=False):
    booking = {
    }

    if number_of_people is not None:
        booking["number_of_people"] = number_of_people

    if booking_datetime is not None:
        booking["booking_datetime"] = booking_datetime

    url = BOOKINGS_SERVICE+"bookings/"+str(booking_id)

    if entrance:
        url += "?entrance=true"

    return _put(url,booking)

def delete_booking(id):
    return _delete(BOOKINGS_SERVICE+"bookings/"+str(id))