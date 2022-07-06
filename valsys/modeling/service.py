import json

from typing import List

from valsys.modeling.client.urls import VSURL
from valsys.modeling.model.fact import Fact
from valsys.utils import logger
from valsys.utils.utils import timeit
from valsys.modeling.models import Permissions
from valsys.modeling.exceptions import TagModelException, ShareModelException
from valsys.spawn.socket_handler import SocketHandler
from valsys.spawn.models import ModelSeedConfigurationData
from valsys.spawn.exceptions import ModelSpawnException
from valsys.modeling.model.model import ModelInformation
from valsys.modeling.model.case import Case
from valsys.modeling.model.module import Module
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.client.service import new_client
from valsys.modeling.client.exceptions import ModelingServicePostException
from valsys.modeling.headers import (
    CASE_ID,
    MODEL_ID,
    UID,
    PARENT_MODULE_ID,
    NAME,
    ORDER,
    MODULE_ID,
)

CODE_POST_SUCCESS = 200


@timeit
def spawn_model(config: ModelSeedConfigurationData, auth_token: str) -> str:
    """
    Given a model config and authentication token, spawn a model.
    Returns the model ID.

    Raises `ModelSpawnException` on errors.
    """
    config.action = "CREATE_MODEL"
    config.validate()
    handler = SocketHandler(config=config.jsonify(),
                            auth_token=auth_token,
                            trace=False)
    handler.run()

    while True:
        if not handler.complete:
            continue
        if handler.error is not None:
            raise ModelSpawnException(f"error building model: {handler.error}")
        elif handler.resp is not None:
            model_id = handler.resp["data"][UID]
        break

    if handler.succesful:
        return model_id

    if handler.exception is not None:
        raise ModelSpawnException(str(handler.exception))
    raise ModelSpawnException("unknown spawn error")


def tag_model(model_id: str, tags: List[str], auth_token: str = None):
    """Tag the machine models"""

    client = new_client(auth_token)
    try:
        return client.post(
            url=VSURL.MODELING_MODEL_PROPERTIES,
            data={
                MODEL_ID: model_id,
                "modelTags": tags,
                "update": True,
                "rollForward": True,
            },
        )
    except ModelingServicePostException as err:
        raise TagModelException(
            f'failed to tag models via call {VSURL.MODELING_MODEL_PROPERTIES}; got {err.status_code} expected {CODE_POST_SUCCESS}; message={err.data}'
        )


def share_model(model_id: str,
                email: str,
                permission: str,
                auth_token: str = None):
    """Share models with the team"""

    client = new_client(auth_token)
    if permission == Permissions.VIEW:
        permissions = {
            "view": True,
        }
    else:
        permissions = {
            "edit": True,
        }

    try:
        client.post(
            url=VSURL.USERS_SHARE_MODEL,
            headers={
                "email": email,
                MODEL_ID: model_id,
            },
            data=permissions,
        )
    except ModelingServicePostException as err:
        raise ShareModelException(f"failed to share models {str(err)}")


@timeit
def pull_model_information(uid: str) -> ModelInformation:
    """Pulls the model information for the UID."""
    client = new_client()
    resp = client.get(
        url=VSURL.MODEL_INFO,
        headers={
            MODEL_ID: uid,
        },
    )
    cases = resp["data"]["model"]
    return ModelInformation.from_json(uid, cases)


@timeit
def pull_case(uid: str) -> Case:
    """Retreive a `Case` by its uid."""
    client = new_client()
    resp = client.get(
        url=VSURL.CASE,
        headers={
            CASE_ID: uid,
        },
    )
    return Case.from_json(resp["data"]["case"])


def recalculate_model(uid: str):
    """Recalculates the model"""
    client = new_client()

    resp = client.get(
        url=VSURL.RECALC_MODEL,
        headers={
            UID: uid,
        },
    )
    if resp.status_code != 200:
        print(resp.json())


def remove_module(model_id, case_id, module_id, parent_module_id):

    client = new_client()
    resp = client.post(
        url=VSURL.DELETE_MODULE,
        data={
            CASE_ID: case_id,
            MODEL_ID: model_id,
            PARENT_MODULE_ID: parent_module_id,
            UID: module_id,
        },
    )
    if resp.status_code != 200:
        print(resp.json())
    else:
        print("removed module")


@timeit
def add_child_module(parent_module_id: str, name: str, model_id: str,
                     case_id: str) -> Module:
    """Add a new module to the parent module.

    Returns the newly constructed `Module` object."""
    logger.info(f"adding child module {name} to parent {parent_module_id} for model {model_id}")
    client = new_client()
    resp = client.post(
        url=VSURL.ADD_MODULE,
        data={
            CASE_ID: case_id,
            MODEL_ID: model_id,
            NAME: name,
            PARENT_MODULE_ID: parent_module_id,
        },
    )

    child_modules = resp["data"]["module"]["childModules"]
    for module in child_modules:
        if module["name"] == name:
            return Module.from_json(module)
    raise ValueError(f"Error adding child module")


@timeit
def add_item(case_id, model_id, name, order, module_id) -> LineItem:
    logger.info(f'adding line item=<{name}> order=<{order}> to modelID={model_id}')
    client = new_client()

    resp = client.post(
        url=VSURL.ADD_ITEM,
        data={
            CASE_ID: case_id,
            MODEL_ID: model_id,
            NAME: name,
            ORDER: order,
            MODULE_ID: module_id,
        },
    )

    module = Module.from_json(resp["data"]["module"])
    for l in module.line_items:
        if l.name == name:
            return l
    raise ValueError(f"cannot find module with name {name}")


def edit_facts(url: str, case_id: str, model_id: str, facts: List[Fact]):
    client = new_client()

    resp = client.post(
        url=url,
        data={
            CASE_ID: case_id,
            MODEL_ID: model_id,
            "forecastIncrement": 1,
            "facts": facts,
        },
    )


def edit_format(case_id: str, model_id: str, facts: List[Fact]):
    """Edit the format on the supplied facts."""
    return edit_facts(url=VSURL.EDIT_FORMAT,
                      case_id=case_id,
                      model_id=model_id,
                      facts=facts)


def edit_formula(case_id: str, model_id: str, facts: List[Fact]):
    """Edit the formula on the supplied facts."""
    return edit_facts(url=VSURL.EDIT_FORMULA,
                      case_id=case_id,
                      model_id=model_id,
                      facts=facts)
