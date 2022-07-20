import json
from http import HTTPStatus
from typing import Dict

import requests

from valsys.modeling.client.urls import VSURL
from .authenticate import authenticate2


class Status:
    SUCCESS = 'success'


def authenticate(username: str, password: str) -> str:
    """Authenticate the user/password combination on the server;

    Returns an authentication token."""
    return authenticate2(username=username,
                         password=password,
                         url=VSURL.LOGIN_USERS)


def auth_headers(auth_token: str) -> Dict[str, str]:
    """Return the `content-type` and `Authorization` header dict

    - Puts in the auth token"""
    return {
        "content-type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
