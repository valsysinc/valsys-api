from dataclasses import dataclass
import json
from typing import Dict, Any
from http import HTTPStatus
import requests


from .exceptions import ModelingServiceGetException, ModelingServicePostException


@dataclass
class ModelingServiceHttpClient:
    """
    ModelingServiceClient takes care of
    interfacing to the requests library.

    Also, raises exceptions when API responses
    come back with un-expected status codes.
    """

    auth_token: str = ""
    status_code: int = 0

    def _add_auth_headers(self, hdrs=None):
        hdrs = hdrs or {}
        auth_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}",
        }
        hdrs.update(auth_headers)
        return hdrs

    def get(
        self,
        url: str,
        headers: Dict[str, str] = None,
        expected_status=HTTPStatus.OK,
    ) -> Dict[str, Any]:
        """
        GET data on the client.

        Takes care of the authentication headers.
        """
        headers = headers or {}
        resp = requests.get(
            url=url,
            headers=self._add_auth_headers(headers),
        )
        self.status_code = resp.status_code
        if resp.status_code != expected_status:
            raise ModelingServiceGetException(
                data=resp.json(),
                url=url,
                status_code=resp.status_code,
            )
        return resp.json()

    def post(
        self,
        url: str,
        headers: Dict[str, str] = None,
        data: Dict[str, str] = None,
        expected_status=HTTPStatus.OK,
    ) -> Dict[str, Any]:
        """
        POST data on the client.

        Takes care of the authentication headers.
        """
        headers = headers or {}
        data = data or {}
        resp = requests.post(
            url=url, headers=self._add_auth_headers(headers), data=json.dumps(data)
        )
        self.status_code = resp.status_code

        if resp.status_code != expected_status:
            raise ModelingServicePostException(
                data=resp.json(),
                url=url,
                status_code=resp.status_code,
            )
        return resp.json()
