import json
from http import HTTPStatus
from typing import Dict

import requests

from valsys.modeling.client.urls import VSURL


class Status:
    SUCCESS = 'success'


def authenticate(username: str, password: str) -> str:
    """Authenticate the user/password combination on the server;

    Returns an authentication token."""
    # make the request

    response = requests.get(url=VSURL.LOGIN_USERS,
                            headers={
                                "username": username,
                                "password": password
                            },
                            data=None)
    if response.status_code != HTTPStatus.OK:
        raise ValueError(
            f"cannot send auth request; code={response.status_code}")

    auth_response = json.loads(response.text.encode("utf8"))
    if auth_response.get("status") != Status.SUCCESS:
        raise ValueError(
            f"authentication error: message={auth_response.get('message')}; user={username}"
        )

    return auth_response["data"]['AccessToken']


def auth_headers(auth_token: str) -> Dict[str, str]:
    """Return the `content-type` and `Authorization` header dict

    - Puts in the auth token"""
    return {
        "content-type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
