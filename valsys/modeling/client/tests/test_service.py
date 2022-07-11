from valsys.modeling.client.service import new_client


class TestNewClient:
    def test_http(self):
        auth_token = 't0k3n'
        client = new_client(auth_token=auth_token)
        assert client.auth_token == auth_token
        assert client.status_code == 0
