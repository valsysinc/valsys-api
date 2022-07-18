from valsys.modeling.client.service import new_client, ModelingClientTypes, new_socket_client
from unittest import mock
import pytest

MODULE_PREFIX = "valsys.modeling.client.service"


class TestNewClient:

    @mock.patch(f"{MODULE_PREFIX}.ModelingServiceHttpClient")
    def test_http_is_default(self, mock_ModelingServiceHttpClient):
        auth_token = 't0k3n'
        mock_client = mock.MagicMock()
        mock_ModelingServiceHttpClient.return_value = mock_client
        client = new_client(auth_token=auth_token)
        mock_ModelingServiceHttpClient.assert_called_with(
            auth_token=auth_token)
        assert client == mock_client

    @mock.patch(f"{MODULE_PREFIX}.ModelingServiceSocketClient")
    def test_socket_client_type(self, mock_ModelingServiceSocketClient):
        auth_token = 't0k3n'
        mock_client = mock.MagicMock()
        mock_ModelingServiceSocketClient.return_value = mock_client
        client = new_client(auth_token=auth_token,
                            client=ModelingClientTypes.SOCKET)
        mock_ModelingServiceSocketClient.assert_called_with(
            auth_token=auth_token)
        assert client == mock_client

    @pytest.mark.parametrize("garbage_type", ['garbage', '1', ''])
    def test_garbage_client_type_raises(self, garbage_type):
        auth_token = 't0k3n'
        with pytest.raises(NotImplementedError) as err:
            new_client(auth_token=auth_token, client=garbage_type)
        assert garbage_type in str(err)


class TestNewSocketClient:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_socket_client_type(self, mock_new_client):
        auth_token = 't0k3n'
        mock_client = mock.MagicMock()
        mock_new_client.return_value = mock_client
        client = new_socket_client(auth_token=auth_token)
        mock_new_client.assert_called_with(auth_token=auth_token,
                                           client=ModelingClientTypes.SOCKET)
        assert client == mock_client