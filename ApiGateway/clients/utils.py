
import requests
TIMEOUT = 2

def _get(url):
    """ Makes a get request with a timeout.

    Returns the json object if with the status code (or None, None in case of timeout).
    """
    try:
        r = requests.get(url, timeout=TIMEOUT)
        try:
            return r.json() ,r.status_code
        except:
            return {}, r.status_code  
    except:
        return {},500

def _post(url,json):
    """ Makes a post request with a timeout.

    Returns the json object if with the status code (or None, None in case of timeout).
    """
    try:
        r = requests.post(url, json=json, timeout=TIMEOUT)
        try:
            return r.json() ,r.status_code
        except:
            return {}, r.status_code  
    except:
        return {},500

def _put(url,json):
    """ Makes a put request with a timeout.

    Returns the json object if with the status code (or None, None in case of timeout).
    """
    try:
        r = requests.put(url, json=json, timeout=TIMEOUT)
        try:
            return r.json() ,r.status_code
        except:
            return {}, r.status_code  
    except:
        return {},500

def _delete(url):
    """ Makes a delete request with a timeout.

    Returns the json object if with the status code (or None, None in case of connection error).
    """
    try:
        r = requests.delete(url, timeout=TIMEOUT)
        try:
            return r.json() ,r.status_code
        except:
            return {}, r.status_code  
    except:
        return {},500
