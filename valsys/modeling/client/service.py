from dataclasses import dataclass
from typing import Dict, Protocol

from valsys.auth.service import authenticate
from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.modeling.client.http import ModelingServiceHttpClient
from valsys.modeling.client.socket import ModelingServiceSocketClient


@dataclass
class ModelingClientTypes:
    HTTP = 'http'
    SOCKET = 'socket'


class ModelingClient(Protocol):

    def get(self, url: str, headers: Dict[str, str],
            expected_status: int) -> Dict[str, str]:
        ...

    def post(self, url: str, headers: Dict[str, str], data: Dict[str, str],
             expected_status: int) -> Dict[str, str]:
        ...


def new_client(auth_token: str = None,
               client=ModelingClientTypes.HTTP) -> ModelingClient:
    """Build and return a new modeling service client object.

    By default creates a HTTP client.

    If no `auth_token` is supplied, one is generated, based
    on the available Valsys credentials in environment variables.
    """
    auth_token = auth_token or authenticate(username=API_USERNAME,
                                            password=API_PASSWORD)

    if client == ModelingClientTypes.HTTP:
        return ModelingServiceHttpClient(auth_token=auth_token)
    elif client == ModelingClientTypes.SOCKET:
        return ModelingServiceSocketClient(auth_token=auth_token)
    raise NotImplementedError(f"unknown client type {client}")


def new_socket_client(auth_token: str) -> ModelingClient:
    """Build and return a new socket-type modeling service client object.
    """
    return new_client(auth_token=auth_token, client=ModelingClientTypes.SOCKET)
