from typing import List

from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.modeling.client.exceptions import (
    ModelingServiceGetException,
    ModelingServicePostException,
)
from valsys.modeling.client.service import new_client, new_socket_client
from valsys.modeling.client.urls import VSURL
from valsys.modeling.exceptions import (
    AddChildModuleException,
    AddLineItemException,
    FilterModelsException,
    NewModelGroupsException,
    PullModelGroupsException,
    PullModelInformationException,
    RecalculateModelException,
    RemoveModuleException,
    ShareModelException,
    TagLineItemException,
    TagModelException,
    UpdateModelGroupsException,
)
from valsys.modeling.headers import Headers
from valsys.modeling.model.case import Case
from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.model.model import ModelInformation, Model
from valsys.modeling.model.module import Module
from valsys.modeling.models import (
    ModelDetailInformation,
    ModelGroups,
    ModelsFilter,
    Permissions,
    SpawnedModelInfo,
)
from valsys.seeds.models import OrchestratorConfig
from valsys.spawn.exceptions import ModelSpawnException
from valsys.modeling.exceptions import SpawnModelResponseException
from valsys.utils import logger
from valsys.modeling.vars import Vars
from valsys.modeling.utils import facts_list


class ModelingActions:
    SPAWN_MODELS = "SPAWN_MODELS"
    DYNAMIC_UPDATES = "DYNAMIC_UPDATES"


def filter_user_models(tags: List[str] = None,
                       model_type: str = 'user',
                       max_date: str = "2023-01-31T00:00:00.000Z",
                       min_date: str = "2002-01-01T00:00:00.000Z",
                       tag_filter_type: str = '',
                       geo_filters: List[str] = None,
                       ind_filters: List[str] = None,
                       filter_on: List[str] = None,
                       filter_term: str = '',
                       pagination=1) -> List[ModelDetailInformation]:
    """Search for a set of models, using the provided set of filters for the using user
    
    Args:
        filter_on: List of strings of properties to filter on; allowed: `Name`, `Ticker`, `Geography`, `Industry`.
        filter_term: Will match according the props in the `filter_on` list.  
        model_type: Options are `user`, `shared`, `both`. 
        max_date: Maximum creation date of the model (required format: YYYY-MM-DDTHH:MM:DD.SSSZ)
        min_date: Minimum creation date of the model (required format: YYYY-MM-DDTHH:MM:DD.SSSZ)
        geo_filters: The geographies to include in the search
        ind_filters: The industries to include in the search
        tags: List of tags to filter on
        tag_filter_type: How to combine the tags to search over; options are `and` and `or`.
        pagination: Page number of results
    Returns:
        List of matching model information objects.
    """

    filters = ModelsFilter(
        max_date=max_date,
        min_date=min_date,
        tag_filter_type=tag_filter_type,
        model_type=model_type,
        geo_filters=geo_filters,
        ind_filters=ind_filters,
        tag_filters=tags,
        predicate=filter_term,
    )
    filters.set_filter_on(filter_on)

    headers = {
        'pagination': str(pagination),
    }
    client = new_client()
    try:
        resp = client.post(VSURL.USERS_FILTER_HISTORY,
                           headers=headers,
                           data=filters.jsonify())
    except ModelingServicePostException as err:
        raise err
    return [
        ModelDetailInformation.from_json(j)
        for j in resp.get('data').get('models')
    ]


def spawn_model(config: OrchestratorConfig) -> List[SpawnedModelInfo]:
    """
    Expects
    {
        "models": [
            {
                "status":  "success",
                "modelID": "1234",
                "ticker":  "SBUX"
            }
        ]
    }

    from the socket.
    """
    client = new_socket_client()
    config.action = ModelingActions.SPAWN_MODELS
    try:
        resp = client.post(url=VSURL.SCK_ORCHESTRATOR, data=config.jsonify())
        smi = []
        fds = []
        for m in resp.get('models'):
            if m.get('status') == Vars.SUCCESS:
                smi.append(SpawnedModelInfo.from_json(m))
            else:
                fds.append({
                    'status': m.get('status'),
                    'ticker': m.get('ticker'),
                    'error': m.get('error')
                })
        if len(fds) > 0:
            raise ModelSpawnException(f"error building model: {fds}")
        return smi

    except (ModelingServiceGetException, SpawnModelResponseException,
            Exception) as err:
        raise ModelSpawnException(
            f"error building model: {client.error} {str(err)}")


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
    payload = {
        Headers.MODEL_ID: model_id,
        "tags": tags,
        "update": True,
        "rollForward": True,
    }
    try:
        return client.post(
            url=VSURL.MODELING_MODEL_PROPERTIES,
            data=payload,
        )
    except ModelingServicePostException as err:
        raise TagModelException(
            f'error tagging model via call {VSURL.MODELING_MODEL_PROPERTIES}; got {err.status_code}; message={err.data}'
        )


def tag_line_item(model_id: str, line_item_id: str,
                  tags: List[str]) -> LineItem:
    """Tag a line item.

    Note that this replaces any existing tags on the line item.
    
    Args:
        model_id: The ID of the model containing the line item
        line_item_id: The ID of the line item
        tags: The tags to give to the line item
    
    Returns:
        LineItem

    """
    client = new_client()
    try:
        ait = client.post(
            url=VSURL.ADD_ITEM_TAGS,
            data={
                Headers.MODEL_ID: model_id,
                Headers.LINE_ITEM_ID: line_item_id,
                Headers.TAGS: tags
            },
        )
    except ModelingServicePostException as err:
        raise TagLineItemException(f"error tagging line item: {str(err)}")
    return LineItem.from_json(ait.get('data').get('lineItem'))


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
                          "action": ModelingActions.DYNAMIC_UPDATES,
                          "username": API_USERNAME,
                          "password": API_PASSWORD
                      })
    return resp


def pull_model_groups() -> ModelGroups:
    """Pulls model groups.
    
    Returns a list of `ModelGroup` objects under the `groups` attribute. 
    Each `ModelGroup` has a `uid`, `name`, `user_id`, `model_ids`

    Returns:
        ModelGroups
    """
    client = new_client()
    try:
        g = client.get(url=VSURL.USERS_GROUPS)
    except ModelingServiceGetException as err:
        raise PullModelGroupsException(
            f"error pulling model groups: {str(err)}")
    return ModelGroups.from_json(g.get('data'))


def new_model_groups(group_name: str, model_ids: List[str]) -> ModelGroups:
    """Add a new model group.
    
    Args:
        group_name: The name of the new model group
        model_ids: The IDs of the models to go into the group

    Returns:
        ModelGroups
    """
    client = new_client()
    try:
        g = client.post(url=VSURL.USERS_GROUP,
                        data={
                            'name': group_name,
                            'modelIDs': model_ids
                        })
    except ModelingServicePostException as err:
        raise NewModelGroupsException(
            f"error adding new model groups: {str(err)}")
    return ModelGroups.from_json(g.get('data'))


def update_model_groups(uid: str, name: str,
                        model_ids: List[str]) -> ModelGroups:
    """Updates the models groups.
    
    Args:
        uid: The UID of the model
        name: The name of the model group
        model_ids: The IDs
    
    Returns:
        ModelGroups
    """
    client = new_client()
    try:
        g = client.post(url=VSURL.USERS_UPDATE_GROUP,
                        data={
                            'name': name,
                            'uid': uid,
                            'modelIDs': model_ids
                        })
    except ModelingServicePostException as err:
        raise UpdateModelGroupsException(str(err))

    return ModelGroups.from_json(g.get('data'))


def pull_model_information(model_id: str) -> ModelInformation:
    """Pulls the model information for the `model_id`.
    
    Args:
        model_id: the ID of the required model.
    
    Returns:
        The `ModelInformation` object for the model.
    """
    client = new_client()
    try:
        resp = client.get(
            url=VSURL.MODEL_INFO,
            headers={Headers.MODEL_IDS: model_id},
        )
        cases = resp["data"]["models"][0]['model']

    except (ModelingServiceGetException, Exception) as err:
        raise PullModelInformationException(
            f"could not pull model info for model={model_id}")
    return ModelInformation.from_json(model_id, cases)


def pull_model(model_id: str) -> Model:
    """Pull a model by its ID.
    
    Args:
        model_id: the ID of the required model.
    
    Returns:
        The `Model` object for the model.
    """
    client = new_client()

    resp = client.get(
        url=VSURL.PULL_MODEL,
        headers={"modelId": model_id},
    )
    return Model.from_json(resp.get('data').get('model'))


def pull_model_datasources(model_id: str) -> str:
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


def recalculate_model(model_id: str) -> List[Fact]:
    """Recalculates the model.
    
    Args:
        model_id: The ID of the model to be recalculated.
    
    Returns:
        List of Facts updated during the recalculation process.
    """
    client = new_client()
    payload = {Headers.MODEL_ID: model_id}

    try:
        resp = client.post(url=VSURL.RECALC_MODEL, data=payload)
    except ModelingServicePostException as err:
        raise RecalculateModelException(
            f"error posting model for recalculating: {str(err)}")

    if resp.get('status') == Vars.SUCCESS:
        return facts_list(resp.get('data').get('facts'))
    raise RecalculateModelException(
        f"error recalculating model: {resp.get('error')}")


def remove_module(model_id: str, module_id: str):
    """Removes the specified module from the model.
    
    Args:
        model_id: The ID of the model.
        module_id: The ID of the module to be removed.
    """

    client = new_client()
    try:
        client.post(
            url=VSURL.DELETE_MODULE,
            data={
                Headers.MODEL_ID: model_id,
                Headers.MODULE_ID: module_id,
            },
        )
    except ModelingServicePostException as err:
        raise RemoveModuleException(f'error removing module: {str(err)}')
    return True


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
    payload = {
        Headers.CASE_ID: case_id,
        Headers.MODEL_ID: model_id,
        Headers.NAME: name,
        Headers.PARENT_MODULE_ID: parent_module_id,
    }
    client = new_client()
    resp = client.post(
        url=VSURL.ADD_MODULE,
        data=payload,
    )
    try:
        child_modules = resp["data"]["module"]['edges']["childModules"]
    except KeyError:
        raise AddChildModuleException(
            f"Error adding child module: unexpected data structure")
    for module in child_modules:
        if module["name"] == name:
            return Module.from_json(module)
    raise AddChildModuleException(
        f"Error adding child module: could not find module with name {name}")


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
                Headers.LINE_ITEM_NAME: name,
                Headers.ORDER: order,
                Headers.MODULE_ID: module_id,
            },
        )

    except (ModelingServicePostException, Exception) as err:
        logger.exception(err)
        raise AddLineItemException(
            f"error adding line item to model={model_id} module={module_id}; {str(err)}"
        )
    try:
        line_items = resp["data"]["module"]['edges']['lineItems']
    except KeyError as err:
        raise AddLineItemException(
            "error adding line item: invalid data structure")

    for l in line_items:
        if l['name'] == name:
            return LineItem.from_json(l)

    raise AddLineItemException(
        f"error adding line item: cannot find module with name {name}")


def delete_line_item(model_id: str, module_id: str,
                     line_item_id: str) -> Module:
    client = new_client()

    resp = client.post(
        url=VSURL.DELETE_ITEM,
        data={
            Headers.MODEL_ID: model_id,
            Headers.LINE_ITEM_ID: line_item_id,
            Headers.MODULE_ID: module_id,
        },
    )
    module = Module.from_json(resp.get('data').get('module'))
    return module


def edit_facts(url: str, case_id: str, model_id: str,
               facts: List[Fact]) -> List[Fact]:
    client = new_client()
    payload = {
        Headers.CASE_ID: case_id,
        Headers.MODEL_ID: model_id,
        "forecastIncrement": 1,
        "facts": facts,
    }
    resp = client.post(
        url=url,
        data=payload,
    )
    if resp.get('status') != Vars.SUCCESS:
        raise Exception(f'fact editing {resp.get("error")}')
    return facts_list(resp.get('data').get('facts'))


def edit_format(case_id: str, model_id: str, facts: List[Fact]):
    """Edit the format on the supplied facts."""
    return edit_facts(url=VSURL.EDIT_FORMAT,
                      case_id=case_id,
                      model_id=model_id,
                      facts=facts)


def edit_formula(case_id: str, model_id: str, facts: List[Fact]) -> List[Fact]:
    """Edit the formula on the supplied facts.
    
    Args:
        case_id: The caseID for where the facts live.
        model_id: The modelID for where the facts live.
        facts: The list of facts whose formulae are to be edited.

    
    Returns:
        List of `Fact`s modified by the edit.
    """
    return edit_facts(url=VSURL.EDIT_FORMULA,
                      case_id=case_id,
                      model_id=model_id,
                      facts=facts)
