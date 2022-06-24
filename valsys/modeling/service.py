import json
from typing import List
import requests
from valsys.config import (
    URL_MODELING_MODEL_PROPERTIES,
    URL_USERS_SHARE_MODEL,
    URL_USERS_MODELS,
)
from valsys.auth.service import auth_headers
from valsys.modeling.models import Permissions
from valsys.modeling.exceptions import TagModelException, ShareModelException
from valsys.spawn.socket_handler import SocketHandler
from valsys.spawn.models import ModelSeedConfigurationData
from valsys.spawn.exceptions import ModelSpawnException

CODE_POST_SUCCESS = 200


def spawn_model(config: ModelSeedConfigurationData, auth_token: str):
    """
    Given a model config and authentication token, spawn a model.
    Returns the model ID.

    Raises `ModelSpawnException` on errors.
    """
    config.action = "CREATE_MODEL"
    config.validate()
    handler = SocketHandler(config=config.jsonify(), auth_token=auth_token, trace=False)
    handler.run()

    while True:
        if not handler.complete:
            continue
        if handler.error is not None:
            raise ModelSpawnException(f"error building model: {handler.error}")
        elif handler.resp is not None:
            model_id = handler.resp["data"]["uid"]
        break

    if handler.succesful:
        return model_id

    if handler.exception is not None:
        raise ModelSpawnException(str(handler.exception))
    raise ModelSpawnException("unknown spawn error")


def tag_model(model_id: str, tags: List[str], auth_token: str):
    """Tag the machine models"""

    # make request

    body = {"modelID": model_id, "modelTags": tags, "update": True, "rollForward": True}
    response = requests.post(
        url=URL_MODELING_MODEL_PROPERTIES,
        headers=auth_headers(auth_token),
        data=json.dumps(body),
    )
    if response.status_code != CODE_POST_SUCCESS:
        raise TagModelException(
            f'failed to tag models via call {URL_MODELING_MODEL_PROPERTIES}; got {response.status_code} expected {CODE_POST_SUCCESS}; message={json.loads(response.content).get("message")}'
        )
    return response


def share_model(model_id: str, email: str, permission: str, auth_token: str):
    """Share models with the team"""
    # authenticated header
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + auth_token,
        "email": email,
        "modelID": model_id,
    }

    # make request

    if permission == Permissions.VIEW:
        permissions = {
            "view": True,
        }
    else:
        permissions = {
            "edit": True,
        }

    response = requests.post(
        url=URL_USERS_SHARE_MODEL, headers=headers, data=json.dumps(permissions)
    )

    if response.status_code != CODE_POST_SUCCESS:

        raise ShareModelException(
            f'failed to share models via call {URL_USERS_SHARE_MODEL}; expected={CODE_POST_SUCCESS} got={response.status_code}; message={json.loads(response.content).get("message")}'
        )


def delete_models(model_id_lst: List[str], auth_token: str):

    # make request
    body = {
        "models": model_id_lst,
    }
    response = requests.delete(
        url=URL_USERS_MODELS, headers=auth_headers(auth_token), data=json.dumps(body)
    )
    print("models dropped")
