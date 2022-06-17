import json

import requests
from valsys.config import URL_MODELING_MODEL_PROPERTIES, URL_USERS_SHARE_MODEL


def tag_models(modelID, tags, auth_token):
    """Tag the machine models"""
    # authenticated header
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer "+auth_token
    }

    # make request

    body = {
        "modelID": modelID,
        "modelTags": tags,
        "update": True,
        "rollForward": True
    }
    response = requests.post(
        url=URL_MODELING_MODEL_PROPERTIES, headers=headers, data=json.dumps(body))


def share_model(modelID, userEmail, permission, auth_token):
    """Share models with the team"""
    # authenticated header
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer "+auth_token,
        "email": userEmail,
        "modelID": modelID
    }

    # make request

    if permission == "view":
        permissions = {
            "view": True,
        }
    else:
        permissions = {
            "edit": True,
        }

    response = requests.post(
        url=URL_USERS_SHARE_MODEL, headers=headers, data=json.dumps(permissions))
    print("Shared model with:", userEmail)
