import json
from collections import namedtuple
from http import HTTPStatus

import requests
from valsys.modeling.client.urls import VSURL


def authenticate(username: str, password: str) -> str:
    """Authenticate the user/password combination on the server;

    Returns an authentication token."""
    # make the request
    headers = {"username": username, "password": password}

    # decode into an object and validate
    response = requests.get(url=VSURL.LOGIN_USERS, headers=headers, data=None)
    if response.status_code != HTTPStatus.OK:
        raise ValueError(f"cannot send auth request; code={response.status_code}")
    auth_response = json.loads(
        response.text.encode("utf8"),
        object_hook=lambda d: namedtuple("X", d.keys())(*d.values()),
    )
    if auth_response.status != "success":
        raise ValueError(
            f"AUTHENTICATION ERROR: {auth_response.message}; user={username}"
        )

    # set access token as environment variable
    return auth_response.data.AccessToken


def auth_headers(auth_token: str):
    """Return the `content-type` and `Authorization` header dict

    - Puts in the auth token"""
    return {"content-type": "application/json", "Authorization": f"Bearer {auth_token}"}
