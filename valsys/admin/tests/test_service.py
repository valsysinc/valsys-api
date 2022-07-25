from valsys.admin.service import try_login, gen_login_url
from unittest import mock

MODULE_PREFIX = "valsys.admin.service"


class TestTryLogin:

    @mock.patch(f"{MODULE_PREFIX}.authenticate2")
    def test_works_ok(self, mock_authenticate2):
        base = 'base'
        user = 'user'
        password = 'pw'
        mock_authenticate2.return_value = True
        assert try_login(base, user, password) is True
        mock_authenticate2.assert_called_once_with(user,
                                                   password,
                                                   url=gen_login_url(base))

    @mock.patch(f"{MODULE_PREFIX}.authenticate2")
    def test_no_auth(self, mock_authenticate2):
        base = 'base'
        user = 'user'
        password = 'pw'
        mock_authenticate2.side_effect = Exception

        assert try_login(base, user, password) is False
