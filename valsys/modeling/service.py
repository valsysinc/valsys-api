from dataclasses import dataclass
from typing import List

from valsys.modeling.client.exceptions import (
    ModelingServiceGetException,
    ModelingServicePostException,
)
from valsys.modeling.client.service import new_client, new_socket_client
from valsys.modeling.client.urls import VSURL
from valsys.modeling.exceptions import ShareModelException, TagModelException
from valsys.modeling.headers import Headers
from valsys.modeling.model.case import Case
from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.model.model import ModelInformation
from valsys.modeling.model.module import Module
from valsys.modeling.models import Permissions
from valsys.seeds.models import OrchestratorConfig
from valsys.spawn.exceptions import ModelSpawnException
from valsys.utils import logger


CODE_POST_SUCCESS = 200
SPAWN_MODELS_ACTION = "SPAWN_MODELS"


@dataclass
class SpawnedModelInfo:
    model_id: str
    ticker: str

    @classmethod
    def from_json(cls, m):
        return cls(model_id=m.get('modelID'), ticker=m.get('ticker'))


def spawn_model(config: OrchestratorConfig) -> List[SpawnedModelInfo]:
    client = new_socket_client()
    config.action = SPAWN_MODELS_ACTION
    try:
        resp = client.post(url=VSURL.SCK_ORCHESTRATOR, data=config.jsonify())
        return [
            SpawnedModelInfo.from_json(m) for m in resp.get('models')
            if m.get('status') == 'success'
        ]
    except (ModelingServiceGetException, Exception):
        raise ModelSpawnException(f"error building model: {client.error}")


def tag_model(model_id: str, tags: List[str], auth_token: str = None):
    """Tag the model with `model_id` with the list of `tags`.
    
    Note that this removes any existing tags;
    if you wanted to append tags, use the `append_tags` function.

    Args:
        model_id: ID of the model to add tags to
        tags: List of tags to add to the model
        auth_token: Optional authentication token
    """

    client = new_client(auth_token)
    try:
        return client.post(
            url=VSURL.MODELING_MODEL_PROPERTIES,
            data={
                Headers.MODEL_ID: model_id,
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
    """Share model to another user.
    
    Args:
         model_id: ID of the model to share
         email: The email address of the user to share the model with
         permission: The permissions to give to the user
    """

    client = new_client(auth_token)
    permissions = Permissions(permission)

    try:
        client.post(
            url=VSURL.USERS_SHARE_MODEL,
            headers={
                "email": email,
                Headers.MODEL_ID: model_id,
            },
            data=permissions.jsonify(),
        )
    except ModelingServicePostException as err:
        raise ShareModelException(f"failed to share models {str(err)}")


def dynamic_updates():
    """Requests dynamic updates are executed."""
    client = new_socket_client()

    resp = client.get(url=VSURL.SCK_ORCHESTRATOR,
                      data={
                          "action": "DYNAMIC_UPDATES",
                      })
    return resp


def pull_model_information(model_id: str) -> ModelInformation:
    """Pulls the model information for the `model_id`.
    
    Args:
        model_id: the ID of the required model.
    
    Returns:
        The `ModelInformation` object for the model.
    """
    client = new_client()
    resp = client.get(
        url=VSURL.MODEL_INFO,
        headers={
            Headers.MODEL_ID: model_id,
        },
    )
    cases = resp["data"]["model"]

    return ModelInformation.from_json(model_id, cases)


def pull_model_datasources(model_id) -> str:
    """Pull the model data source string for the `model_id`."""
    return pull_model_information(model_id).data_sources


def pull_case(case_id: str) -> Case:
    """Retreive a `Case` by its uid.
    
    Args:
        case_id: the case's UID
    
    Returns:
        The appropriate `Case` object.
    """
    client = new_client()
    resp = client.get(
        url=VSURL.CASE,
        headers={
            Headers.CASE_ID: case_id,
        },
    )
    return Case.from_json(resp["data"]["case"])


def get_model_tags(uid: str) -> List[str]:
    """Get the list of tags for the model."""
    model_info = pull_model_information(uid)
    return model_info.tags


def append_tags(uid: str, tags: List[str]):
    curr_tags = get_model_tags(uid)
    tag_model(uid, list(set(tags).union(set(curr_tags))))


def recalculate_model(model_id: str):
    """Recalculates the model.
    
    Args:
        model_id: The ID of the model to be recalculated.
    """
    client = new_socket_client()

    resp = client.get(url=VSURL.RECALC_MODEL,
                      data={
                          "action": "RECALCULATE_MODEL",
                          "uid": model_id
                      },
                      after_token=model_id)
    return resp


def remove_module(model_id: str, case_id: str, module_id: str,
                  parent_module_id: str):

    client = new_client()
    client.post(
        url=VSURL.DELETE_MODULE,
        data={
            Headers.CASE_ID: case_id,
            Headers.MODEL_ID: model_id,
            Headers.PARENT_MODULE_ID: parent_module_id,
            Headers.UID: module_id,
        },
    )


def add_child_module(parent_module_id: str, name: str, model_id: str,
                     case_id: str) -> Module:
    """Add a new module to the parent module.

    Args:
        parent_module_id: The moduleID of the parent
        name: The name of the new module
        model_id: The ID of the model into which the module is to be inserted
        case_id: The caseID of the module.

    Returns:
        The newly constructed `Module` object.
    """

    client = new_client()
    resp = client.post(
        url=VSURL.ADD_MODULE,
        data={
            Headers.CASE_ID: case_id,
            Headers.MODEL_ID: model_id,
            Headers.NAME: name,
            Headers.PARENT_MODULE_ID: parent_module_id,
        },
    )

    child_modules = resp["data"]["module"]["childModules"]
    for module in child_modules:
        if module["name"] == name:
            return Module.from_json(module)
    raise ValueError(f"Error adding child module")


def add_line_item(case_id: str, model_id: str, module_id: str, name: str,
                  order: int) -> LineItem:
    """Add a line item to an existing module.
    
    Args:
        case_id: The caseID of the model
        model_id: The modelID
        module_id: The ID of the module for the new line item
        name: Name of the line item
        order: Order of the line item in the module

    Returns:
        The newly created `LineItem` object.
    """

    client = new_client()
    try:
        resp = client.post(
            url=VSURL.ADD_ITEM,
            data={
                Headers.CASE_ID: case_id,
                Headers.MODEL_ID: model_id,
                Headers.NAME: name,
                Headers.ORDER: order,
                Headers.MODULE_ID: module_id,
            },
        )
    except ModelingServicePostException as err:
        logger.exception(err)
        raise

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
            Headers.CASE_ID: case_id,
            Headers.MODEL_ID: model_id,
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
    """Edit the formula on the supplied facts.
    
    Args:
        case_id: The caseID for where the facts live.
        model_id: The modelID for where the facts live.
        facts: The list of facts whose formulae are to be edited.
    """
    return edit_facts(url=VSURL.EDIT_FORMULA,
                      case_id=case_id,
                      model_id=model_id,
                      facts=facts)
