from dataclasses import dataclass
from valsys.auth.service import authenticate
from valsys.config import API_PASSWORD, API_USERNAME

from valsys.modeling.client.http import ModelingServiceHttpClient
from valsys.modeling.client.socket import ModelingServiceSocketClient


@dataclass
class ModelingClientTypes:
    HTTP = 'http'
    SOCKET = 'socket'


def new_client(auth_token: str = None, client='http') -> ModelingServiceHttpClient:
    """Build and return a new modeling service client object.

    If no `auth_token` is supplied, one is generated, based
    on the available Valsys credentials in environment variables.
    """
    auth_token = auth_token or authenticate(
        username=API_USERNAME, password=API_PASSWORD
    )

    if client == ModelingClientTypes.HTTP:
        return ModelingServiceHttpClient(auth_token=auth_token)
    elif client == ModelingClientTypes.SOCKET:
        return ModelingServiceSocketClient(auth_token=auth_token)
    raise NotImplementedError(f"unknown client type {client}")
