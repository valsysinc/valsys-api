import json
from typing import List
import requests
from valsys.config import (
    URL_MODELING_MODEL_PROPERTIES,
    URL_USERS_SHARE_MODEL,
    URL_MODEL_INFO,
    URL_RECALC_MODEL,
    URL_CASE,
    URL_DELETE_MODULE,
    URL_ADD_ITEM,
    URL_ADD_MODULE,
    URL_EDIT_FORMAT,
    URL_EDIT_FORMULA,
)
from valsys.auth.service import auth_headers

from valsys.modeling.models import Permissions
from valsys.modeling.exceptions import TagModelException, ShareModelException
from valsys.spawn.socket_handler import SocketHandler
from valsys.spawn.models import ModelSeedConfigurationData
from valsys.spawn.exceptions import ModelSpawnException
from valsys.modeling.model.case import Case

CODE_POST_SUCCESS = 200


def spawn_model(config: ModelSeedConfigurationData, auth_token: str) -> str:
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
        "Authorization": f"Bearer {auth_token}",
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


def pull_model_information(auth_token: str, uid: str) -> str:
    """Pulls the first case uid in a model"""
    path = URL_MODEL_INFO
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
        "modelID": uid,
    }
    resp = requests.get(url=path, headers=headers)
    if resp.status_code != 200:
        print(resp.json())
    return resp.json()["data"]["model"]["cases"][0]["uid"]


def recalculate_model(auth_token: str, uid: str):
    """Recalculates the model"""
    path = URL_RECALC_MODEL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
        "uid": uid,
    }
    resp = requests.get(url=path, headers=headers)
    if resp.status_code != 200:
        print(resp.json())


def pull_case(auth_token, uid: str) -> Case:
    path = URL_CASE
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
        "caseID": uid,
    }
    resp = requests.get(url=path, headers=headers)
    if resp.status_code != 200:
        print(resp.json())
    case = Case.from_json(resp.json()["data"]["case"])
    return case


def remove_module(auth_token, modelID, caseID, moduleID, parentModuleID, module_name):
    path = URL_DELETE_MODULE
    body = {
        "token": auth_token,
        "caseID": caseID,
        "modelID": modelID,
        "parentModuleID": parentModuleID,
        "uid": moduleID,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }
    resp = requests.post(url=path, headers=headers, data=json.dumps(body))
    if resp.status_code != 200:
        print(resp.json())
    else:
        print("removed module")


def add_child_module(parent_module_id, name, modelID, caseID):
    auth_token = None
    path = URL_ADD_MODULE
    body = {
        "token": auth_token,
        "caseID": caseID,
        "modelID": modelID,
        "name": name,
        #             "unlinked": True,
        "parentModuleID": parent_module_id,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }
    resp = requests.post(url=path, headers=headers, data=json.dumps(body))
    if resp.status_code != 200:
        print(resp.json())
    child_modules = resp.json()["data"]["module"]["childModules"]
    print("Created New Module: {}".format(name))
    for module in child_modules:
        if module["name"] == name:
            return module


def add_item(case_id, model_id, name, order, module_id):
    auth_token = None
    path = URL_ADD_ITEM
    body = {
        "token": auth_token,
        "caseID": case_id,
        "modelID": model_id,
        "name": name,
        "order": order,
        "moduleID": module_id,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }
    resp = requests.post(url=path, headers=headers, data=json.dumps(body))
    if resp.status_code != 200:
        print(resp.json())
    print("Added item:", name)
    return resp.json()["data"]


def edit_format(case_id, model_id, facts):
    auth_token = None
    path = URL_EDIT_FORMAT
    body = {
        "token": auth_token,
        "caseID": case_id,
        "modelID": model_id,
        "forecastIncrement": 1,
        "facts": facts,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }
    resp = requests.post(url=path, headers=headers, data=json.dumps(body))
    if resp.status_code != 200:
        print(resp.json())


def edit_formula(case_id, model_id, facts):
    auth_token = None
    path = URL_EDIT_FORMULA
    body = {
        "token": auth_token,
        "caseID": case_id,
        "modelID": model_id,
        "forecastIncrement": 1,
        "facts": facts,
    }

    params = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }
    resp = requests.post(url=path, headers=params, data=json.dumps(body))
    if resp.status_code != 200:
        print(resp.json())
