from unittest import mock

from valsys.modeling.client.socket_handler import (
    TRACE_DEFAULT,
    SocketHandler,
    States,
    Status,
)


MODULE_PREFIX = "valsys.modeling.client.socket_handler"


class TestSocketHandler:

    @mock.patch(f"{MODULE_PREFIX}.websocket")
    def test_init_ok(self, mock_websocket):
        url, config, auth_token = 'u', {'info': 42}, 't0k3n'
        sh = SocketHandler(url=url, config=config, auth_token=auth_token)
        assert sh.url == f"{url}/"
        assert sh.config == config
        mock_websocket.enableTrace.assert_called_once_with(TRACE_DEFAULT)
        assert sh.status == Status.UNKNOWN
        assert sh.state == States.IN_PROGRESS
        mock_websocket.WebSocketApp.assert_called_once()
        assert not sh.complete
        assert not sh.succesful
        _, kw = mock_websocket.WebSocketApp.call_args
        assert kw.get('url') == f"{url}/{auth_token}"

    @mock.patch(f"{MODULE_PREFIX}.websocket")
    def test_init_ok_dont_add(self, mock_websocket):
        url, config, auth_token = 'u/', {'info': 42}, 't0k3n'
        sh = SocketHandler(url=url, config=config, auth_token=auth_token)
        assert sh.url == url
        assert sh.config == config
        mock_websocket.enableTrace.assert_called_once_with(TRACE_DEFAULT)
        assert sh.status == Status.UNKNOWN
        assert sh.state == States.IN_PROGRESS
        mock_websocket.WebSocketApp.assert_called_once()
        assert not sh.complete
        assert not sh.succesful
        _, kw = mock_websocket.WebSocketApp.call_args
        assert kw.get('url') == f"{url}{auth_token}"

    @mock.patch(f"{MODULE_PREFIX}.websocket")
    def test_init_ok_with_after_token(self, mock_websocket):
        url, config, auth_token = 'u', {'info': 42}, 't0k3n'
        after_token = 'hello'
        sh = SocketHandler(url=url,
                           config=config,
                           auth_token=auth_token,
                           after_token=after_token)
        assert sh.url == f"{url}/"
        assert sh.config == config
        mock_websocket.enableTrace.assert_called_once_with(TRACE_DEFAULT)
        assert sh.status == Status.UNKNOWN
        assert sh.state == States.IN_PROGRESS
        mock_websocket.WebSocketApp.assert_called_once()
        assert not sh.complete
        assert not sh.succesful
        _, kw = mock_websocket.WebSocketApp.call_args
        assert kw.get('url') == f"{url}/{auth_token}/{after_token}"
