from dataclasses import dataclass
import requests
import json

from typing import Dict
from http import HTTPStatus


class ModelingServiceGetException(Exception):
    def __init__(self, message, **kwargs) -> None:
        self.url = kwargs.get("url")
        super().__init__(message)


@dataclass
class ModelingServiceClient:
    auth_token: str = ""

    def _add_auth_headers(self, hdrs):
        auth_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}",
        }
        hdrs.update(auth_headers)
        return hdrs

    def get(self, url: str, headers: Dict[str, str]):
        """
        GET data on the client.

        Takes care of the authentication headers.
        """
        headers = headers or {}
        resp = requests.get(
            url=url,
            headers=self._add_auth_headers(headers),
        )
        if resp.status_code != HTTPStatus.OK:
            raise ModelingServiceGetException(
                f"code={resp.status_code}; {resp.json()}", url=url
            )
        return resp.json()

    def post(self, url: str, headers: Dict[str, str] = None, data=None):
        headers = headers or {}
        data = data or {}
        resp = requests.post(
            url=url, headers=self._add_auth_headers(headers), data=json.dumps(data)
        )
        return resp
