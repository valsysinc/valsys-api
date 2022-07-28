from unittest import mock

import pytest

from valsys.admin.service import gen_fields, gen_login_url, try_login

MODULE_PREFIX = "valsys.admin.service"


class TestTryLogin:

    @mock.patch(f"{MODULE_PREFIX}.authenticate2")
    def test_works_ok(self, mock_authenticate2):
        base = 'base'
        user = 'user'
        password = 'pw'
        mock_authenticate2.return_value = True
        assert try_login(base, user, password) is None
        mock_authenticate2.assert_called_once_with(user,
                                                   password,
                                                   url=gen_login_url(base))

    @mock.patch(f"{MODULE_PREFIX}.authenticate2")
    def test_no_auth(self, mock_authenticate2):
        base = 'base'
        user = 'user'
        password = 'pw'
        mock_authenticate2.side_effect = Exception

        with pytest.raises(Exception):
            try_login(base, user, password)


class TestGenFields:

    @pytest.mark.parametrize("protocol,host,genfields",
                             [('http', 'you.com', {
                                 'VALSYS_API_SOCKET': 'ws://you.com',
                                 'VALSYS_API_SERVER': 'http://you.com'
                             }),
                              ('https', 'you.com', {
                                  'VALSYS_API_SOCKET': 'wss://you.com',
                                  'VALSYS_API_SERVER': 'https://you.com'
                              }),
                              ('http', 'http://you.com', {
                                  'VALSYS_API_SOCKET': 'ws://you.com',
                                  'VALSYS_API_SERVER': 'http://you.com'
                              }),
                              ('https', 'https://you.com', {
                                  'VALSYS_API_SOCKET': 'wss://you.com',
                                  'VALSYS_API_SERVER': 'https://you.com'
                              })])
    def test_works_ok(self, protocol, host, genfields):
        assert gen_fields(protocol=protocol, host=host) == genfields
