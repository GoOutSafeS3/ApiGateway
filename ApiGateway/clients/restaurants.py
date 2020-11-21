import datetime

from ApiGateway.clients.utils import _get, _post, _put, _delete

RESTAURANTS_SERVICE = "http://restaurants:8080"


def get_restaurants(name=None, opening_time=None, open_day=None, cuisine_type=None, menu=None):
    url = RESTAURANTS_SERVICE+"/restaurants?"

    if name is not None:
        url += "name="+str(name)+"&"

    if opening_time is not None:
        url += "opening_time="+str(opening_time)+"&"

    if open_day is not None:
        url += "open_day="+str(open_day)+"&"

    if cuisine_type is not None:
        url += "cuisine_type="+str(cuisine_type)+"&"

    if menu is not None:
        url += "menu="+str(menu)+"&"

    if url[-1] == "&":
        url = url[:-1]

    if url[-1] == "?":
        url = url[:-1]

    return _get(url)

def post_restaurants(json):
    url = RESTAURANTS_SERVICE + '/restaurants'
    return _post(url=url, json=json)

def get_restaurant(restaurant_id):
    url = RESTAURANTS_SERVICE + '/restaurants/%d'%restaurant_id
    return _get(url=url)

def put_restaurant(restaurant_id, json):
    url = RESTAURANTS_SERVICE + '/restaurants/%d'%restaurant_id
    return _put(url=url, json=json)

def delete_restaurant(restaurant_id):
    url = RESTAURANTS_SERVICE + '/restaurants/%d'%restaurant_id
    return _delete(url=url)

def get_restaurant_rating(restaurant_id):
    url = RESTAURANTS_SERVICE + '/restaurants/%d.rate'%restaurant_id
    return _get(url=url)

def post_restaurant_rating(restaurant_id,json):
    url = RESTAURANTS_SERVICE + '/restaurants/%d/rate'%restaurant_id
    return _post(url=url, json=json)

def get_restaurant_tables(restaurant_id, json, capacity=None):
    url = RESTAURANTS_SERVICE + '/restaurants/%d/tables?'%restaurant_id
    if capacity is not None:
        url += "capacity="+str(capacity)+"&"

    if url[-1] == "&":
        url = url[:-1]

    if url[-1] == "?":
        url = url[:-1]

    return _get(url=url, json=json)

def post_restaurant_table(restaurant_id, json):
    url = RESTAURANTS_SERVICE + '/restaurants/%d/tables'%restaurant_id
    return _post(url=url, json=json)

def get_restaurant_table(restaurant_id, table_id):
    url = RESTAURANTS_SERVICE + '/restaurants/%d/tables/%d'%(restaurant_id,table_id)
    return _get(url=url)

def put_restaurant_table(restaurant_id, table_id, json):
    url = RESTAURANTS_SERVICE + '/restaurants/%d/tables/%d'%(restaurant_id,table_id)
    return _put(url=url, json=json)

def delete_restaurant_table(restaurant_id, table_id):
    url = RESTAURANTS_SERVICE + '/restaurants/%d/tables/%d'%(restaurant_id,table_id)
    return _delete(url=url)