import json
from http import HTTPStatus
from unittest import mock

import pytest

from valsys.auth.service import Status, auth_headers, authenticate


MODULE_PREFIX = "valsys.auth.service"


class TestAuthenticate:

    @mock.patch(f"{MODULE_PREFIX}.requests.get")
    def test_works_ok(self, mock_get):
        username, password = 'username', 'password'
        fake_access_token = 42
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.text = json.dumps({
            "data": {
                "AccessToken": fake_access_token
            },
            "status": Status.SUCCESS
        })

        assert authenticate(username=username,
                            password=password) == fake_access_token
        mock_get.assert_called_once()
        _, kw = mock_get.call_args
        url = kw.get('url')
        assert kw.get('headers') == {
            "username": username,
            "password": password
        }
        assert isinstance(url, str)
        assert url is not ""

    @mock.patch(f"{MODULE_PREFIX}.requests.get")
    def test_req_not_200(self, mock_get):
        username, password = 'username', 'password'
        fake_bad_response_code = HTTPStatus.BAD_GATEWAY
        mock_get.return_value.status_code = fake_bad_response_code
        with pytest.raises(ValueError) as err:
            authenticate(username=username, password=password)
        assert str(fake_bad_response_code.value) in str(err)

    @mock.patch(f"{MODULE_PREFIX}.requests.get")
    def test_req_not_success(self, mock_get):
        username, password = 'username', 'password'

        fake_message = 'garbage'
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.text = json.dumps({
            "status": "garbage",
            "message": fake_message
        })
        with pytest.raises(ValueError) as err:
            authenticate(username=username, password=password)
        assert username in str(err)
        assert fake_message in str(err)


class TestAuthHeaders:

    def test_works_ok(self):
        auth_token = 't0k3n'
        assert auth_headers(auth_token=auth_token) == {
            "content-type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
