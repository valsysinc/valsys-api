from valsys.auth.service import authenticate
from valsys.config import API_PASSWORD, API_USERNAME

from valsys.modeling.client.client import ModelingServiceClient


def new_client(auth_token: str = None) -> ModelingServiceClient:
    """Build and return a new modeling service client object.

    If no `auth_token` is supplied, one is generated, based
    on the available Valsys credentials in environment variables.
    """
    auth_token = auth_token or authenticate(
        username=API_USERNAME, password=API_PASSWORD
    )
    return ModelingServiceClient(auth_token=auth_token)
