import json
from http import HTTPStatus
from typing import Dict

import requests


class Status:
    SUCCESS = 'success'


def authenticate2(username: str, password: str, url) -> str:
    """Authenticate the user/password combination on the server;

    Returns an authentication token."""
    # make the request

    response = requests.get(url=url,
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
