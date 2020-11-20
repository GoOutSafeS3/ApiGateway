from ApiGateway.clients.utils import _get, _post, _delete, _put

USER_SERVICE = "http://users:8081"
TIMEOUT = 1


def get_users(ssn=None, phone=None, email=None, is_positive=None):
    url = USER_SERVICE + '/users?'

    if ssn is not None:
        url += 'ssn=' + str(ssn) + '&'

    if phone is not None:
        url += 'phone=' + str(phone) + '&'

    if email is not None:
        url += 'email=' + str(email) + '&'

    if is_positive is not None:
        url += 'is_positive=True'

    return _get(url=url)


def get_user(user_id):
    url = USER_SERVICE + '/users/' + str(user_id)
    return _get(url=url)


def create_user(dict_user):
    url = USER_SERVICE + '/users'
    return _post(url=url, json=dict_user)


def edit_user(user_id, dict_user):
    url = USER_SERVICE + '/users/'+str(user_id)
    return _put(url=url, json=dict_user)


def delete_user(user_id):
    url = USER_SERVICE + '/users/' + str(user_id)
    return _delete(url)


def get_user_contacts(user_id, begin=None, end=None):
    url = USER_SERVICE + '/users/'+ str(user_id)+'/contacts?'
    if begin is not None and end is not None:
        url+= 'begin='+str(begin)+'&'
        url += 'end=' + str(end)
    return _get(url)
