import json
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Dict

import requests

from valsys.config.config import HOST

from .exceptions import (ModelingServiceGetException,
                         ModelingServicePostException,
                         ModelingServiceDeleteException)


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
        if HOST is not None:
            hdrs.update({"Host": HOST})
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
        if resp.status_code == expected_status:
            return resp.json()
        self.raise_err(ModelingServiceGetException, resp, url)

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

        resp = requests.post(url=url,
                             headers=self._add_auth_headers(headers),
                             data=json.dumps(data), timeout=480)

        self.status_code = resp.status_code
        if resp.status_code == expected_status:
            return resp.json()
        self.raise_err(ModelingServicePostException, resp, url)

    def delete(
        self,
        url: str,
        headers: Dict[str, str] = None,
        data: Dict[str, str] = None,
        expected_status=HTTPStatus.OK,
    ) -> Dict[str, Any]:
        """
        DELETE data on the client.

        Takes care of the authentication headers.
        """
        headers = headers or {}
        data = data or {}

        resp = requests.delete(url=url,
                               headers=self._add_auth_headers(headers),
                               data=json.dumps(data))
        self.status_code = resp.status_code

        if resp.status_code == expected_status:
            return resp.json()
        self.raise_err(ModelingServiceDeleteException, resp, url)

    def raise_err(self, ex: Exception, resp, url: str):
        try:
            d = resp.json()
        except:
            d = {}
        raise ex(
            data=d,
            url=url,
            status_code=resp.status_code,
        )
