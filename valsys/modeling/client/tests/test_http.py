import json
from http import HTTPStatus
from unittest import mock

import pytest

from valsys.modeling.client.exceptions import (
    ModelingServiceGetException,
    ModelingServicePostException,
)
from valsys.modeling.client.http import ModelingServiceHttpClient


MODULE_PREFIX = "valsys.modeling.client.http"


class TestModelingServiceHttpClient:

    def test_init_ok(self):
        msc = ModelingServiceHttpClient()
        assert msc.auth_token == ""

    def test_init_ok_give_auth_token(self):
        token = "Tok3n"
        msc = ModelingServiceHttpClient(token)
        assert msc.auth_token == token

    def test_add_headers_with_nothing(self):
        token = "Tok3n"
        msc = ModelingServiceHttpClient(token)
        hdrs = msc._add_auth_headers()
        assert "Content-Type" in hdrs
        assert "Authorization" in hdrs
        assert token in hdrs.get("Authorization")

    def test_add_headers_with_existing_headers(self):
        token = "Tok3n"
        headers = {"info": 42, "li": [1, 2, 3]}
        msc = ModelingServiceHttpClient(token)
        hdrs = msc._add_auth_headers(headers)
        assert "Content-Type" in hdrs
        assert "Authorization" in hdrs
        assert token in hdrs.get("Authorization")
        assert "info" in hdrs
        assert hdrs.get("li") == [1, 2, 3]

    @mock.patch(f"{MODULE_PREFIX}.requests.get")
    def test_get_with_url_only(self, mock_get):

        fake_reply = {"data": 42}

        mock_response = mock.MagicMock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = fake_reply
        mock_get.return_value = mock_response

        token = "Tok3n"

        msc = ModelingServiceHttpClient(token)
        url = "me"
        reply = msc.get(url)
        mock_get.assert_called_with(
            url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
        )
        mock_response.json.assert_called_once()
        assert reply == fake_reply

    @mock.patch(f"{MODULE_PREFIX}.requests.get")
    def test_get_with_url_and_headers(self, mock_get):

        fake_reply = {"data": 42}

        mock_response = mock.MagicMock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = fake_reply
        mock_get.return_value = mock_response

        token = "Tok3n"

        msc = ModelingServiceHttpClient(token)
        url = "me"
        headers = {"you": 1}
        reply = msc.get(url, headers=headers)
        mock_get.assert_called_with(
            url=url,
            headers={
                "you": 1,
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
        )
        mock_response.json.assert_called_once()
        assert reply == fake_reply

    @pytest.mark.parametrize(
        "bad_code",
        [HTTPStatus.BAD_REQUEST, HTTPStatus.CREATED, HTTPStatus.ACCEPTED])
    @mock.patch(f"{MODULE_PREFIX}.requests.get")
    def test_get_with_url_raises(self, mock_get, bad_code):

        fake_reply = {"data": 42}

        mock_response = mock.MagicMock()
        mock_response.status_code = bad_code
        mock_response.json.return_value = fake_reply
        mock_get.return_value = mock_response

        token = "Tok3n"

        msc = ModelingServiceHttpClient(token)
        url = "me"
        headers = {"you": 1}
        with pytest.raises(ModelingServiceGetException) as err:
            msc.get(url, headers=headers)
        mock_get.assert_called_with(
            url=url,
            headers={
                "you": 1,
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
        )
        assert err.value.url == url
        assert err.value.data == fake_reply
        assert err.value.status_code == bad_code

    @mock.patch(f"{MODULE_PREFIX}.requests.get")
    def test_get_with_url_custom_success_code(self, mock_get):

        fake_reply = {"data": 42}
        expected_status = HTTPStatus.CREATED
        mock_response = mock.MagicMock()
        mock_response.status_code = expected_status
        mock_response.json.return_value = fake_reply
        mock_get.return_value = mock_response

        token = "Tok3n"

        msc = ModelingServiceHttpClient(token)
        url = "me"
        headers = {"you": 1}

        msc.get(url, headers=headers, expected_status=expected_status)
        mock_get.assert_called_with(
            url=url,
            headers={
                "you": 1,
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
        )
        mock_response.json.assert_called_once()

    @pytest.mark.parametrize(
        "bad_code",
        [HTTPStatus.BAD_REQUEST, HTTPStatus.CREATED, HTTPStatus.ACCEPTED])
    @mock.patch(f"{MODULE_PREFIX}.requests.post")
    def test_post_with_url_raises(self, mock_post, bad_code):

        fake_reply = {"data": 42}

        mock_response = mock.MagicMock()
        mock_response.status_code = bad_code
        mock_response.json.return_value = fake_reply
        mock_post.return_value = mock_response

        token = "Tok3n"

        msc = ModelingServiceHttpClient(token)
        url = "me"
        headers = {"you": 1}
        data = {'data': 'info'}
        with pytest.raises(ModelingServicePostException) as err:
            msc.post(url, headers=headers, data=data)
        mock_post.assert_called_with(url=url,
                                     headers={
                                         "you": 1,
                                         "Content-Type": "application/json",
                                         "Authorization": f"Bearer {token}"
                                     },
                                     data=json.dumps((data)), timeout=msc.timeout)
        assert err.value.url == url
        assert err.value.data == fake_reply
        assert err.value.status_code == bad_code
