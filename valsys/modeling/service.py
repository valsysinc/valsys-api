import json
from typing import List
import requests
from valsys.config import URL_MODELING_MODEL_PROPERTIES, URL_USERS_SHARE_MODEL, URL_USERS_MODELS
from valsys.auth.service import auth_headers
from valsys.modeling.models import Permissions
from valsys.modeling.exceptions import TagModelException, ShareModelException
CODE_POST_SUCCESS = 200


def tag_models(model_id: str, tags: List[str], auth_token: str):
    """Tag the machine models"""

    # make request

    body = {
        "modelID": model_id,
        "modelTags": tags,
        "update": True,
        "rollForward": True
    }
    response = requests.post(
        url=URL_MODELING_MODEL_PROPERTIES, headers=auth_headers(auth_token), data=json.dumps(body))
    if response.status_code != CODE_POST_SUCCESS:
        raise TagModelException(
            f'failed to tag models via call {URL_MODELING_MODEL_PROPERTIES}; got {response.status_code} expected {CODE_POST_SUCCESS}')


def share_model(model_id: str, user_email: str, permission: str, auth_token: str):
    """Share models with the team"""
    # authenticated header
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer "+auth_token,
        "email": user_email,
        "modelID": model_id
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
        url=URL_USERS_SHARE_MODEL, headers=headers, data=json.dumps(permissions))
    print("Shared model with:", user_email)
    if response.status_code != CODE_POST_SUCCESS:
        raise ShareModelException(
            f"failed to share models via call {URL_USERS_SHARE_MODEL}; got {response.status_code} expected {CODE_POST_SUCCESS}")


def delete_models(model_id_lst: List[str], auth_token: str):

    # make request
    body = {
        "models": model_id_lst,
    }
    response = requests.delete(url=URL_USERS_MODELS,
                               headers=auth_headers(auth_token),
                               data=json.dumps(body))
    print("models dropped")
