from dataclasses import dataclass
from typing import Any, Dict

from valsys.modeling.client.socket_handler import SocketHandler

from .exceptions import ModelingServiceGetException


@dataclass
class ModelingServiceSocketClient:
    auth_token: str = ""
    error: Any = None

    def run(self, url: str, data: Dict[str, str] = None, after_token=None):
        handler = SocketHandler(url=url,
                                config=data,
                                auth_token=self.auth_token,
                                trace=False,
                                after_token=after_token)

        handler.run()

        while True:
            if not handler.complete:
                continue
            if handler.error is not None:
                self.error = handler.error
                raise Exception(f"{handler.error}")
            elif handler.resp is not None:
                return handler.resp
            break

    def get(self, url: str, data: Dict[str, str] = None, after_token=None):
        return self.run(url, data, after_token=after_token)

    def post(self, url: str, data: Dict[str, str] = None, after_token=None):
        return self.run(url, data, after_token=after_token)
