import requests
import json
from collections import namedtuple
from valsys.config import URL_LOGIN_USERS 

def authenticate(username:str, password:str)->str:
    # make the request
    auth_url =  URL_LOGIN_USERS
    headers = {
      'username': username,
      'password': password
    }

    # decode into an object and validate
    response = requests.request("GET", auth_url, headers=headers, data=None)
    auth_response = json.loads(response.text.encode('utf8'), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    if auth_response.status != "success":
        print("ERROR:", auth_response.message)#
        return
    
    # set access token as environment variable
    return auth_response.data.AccessToken

def headers(auth_token):
    return {
        "content-type": "application/json",
        "Authorization": "Bearer "+auth_token
    }