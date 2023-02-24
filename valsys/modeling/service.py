from typing import List, Dict

from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.modeling.client.exceptions import (
    ModelingServiceGetException,
    ModelingServicePostException,
)
from valsys.modeling.client.service import new_client, new_socket_client
from valsys.modeling.client.urls import VSURL
from valsys.modeling.exceptions import (
    AddChildModuleException, AddLineItemException, NewModelGroupsException,
    PullModelGroupsException, PullModelInformationException,
    RecalculateModelException, RemoveModuleException, ShareModelException,
    SpawnModelResponseException, TagLineItemException, TagModelException,
    UpdateModelGroupsException, DeleteColumnException)
from valsys.modeling.model.group import GroupOfModels
from valsys.modeling.model.case import Case
from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.model.model import Model, ModelInformation
from valsys.modeling.model.module import Module
from valsys.modeling.models import (
    ModelDetailInformationWithFields,
    ModelGroups,
    ModelsFilter,
    Permissions,
    SpawnedModelInfo,
)
from valsys.modeling.utils import facts_list, line_items_list, check_success, module_from_resp
from valsys.modeling.vars import Vars, Headers, Resp
from valsys.seeds.models import OrchestratorConfig
from valsys.spawn.exceptions import ModelSpawnException
from valsys.utils import logger
from valsys.utils.time import tomorrow
from valsys.modeling.model.simulation import SimulationResponse, ModelSimulations


class ModelingActions:
    SPAWN_MODELS = "SPAWN_MODELS"
    DYNAMIC_UPDATES = "DYNAMIC_UPDATES"


def health():
    client = new_client()
    return client.get(url=VSURL.HEALTH, )


def filter_user_models(
        tags: List[str] = None,
        model_type: str = 'user',
        max_date: str = tomorrow(),
        min_date: str = "2002-01-01T00:00:00.000Z",
        tag_filter_type: str = '',
        geo_filters: List[str] = None,
        ind_filters: List[str] = None,
        filter_on: List[str] = None,
        filter_term: str = '',
        pagination: int = 1,
        fields: List[str] = None) -> List[ModelDetailInformationWithFields]:
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
        fields: Fields to return per model
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
    url = VSURL.USERS_FILTER_HISTORY

    if fields is not None:
        filters.add_fields(fields)
        url = VSURL.USERS_FILTER_HISTORY_FIELDS

    headers = {
        Headers.PAGINATION: str(pagination),
    }
    client = new_client()
    try:
        payload = filters.jsonify()
        resp = client.post(url=url, headers=headers, data=payload)
    except ModelingServicePostException as err:
        raise err
    try:
        return [
            ModelDetailInformationWithFields.from_json(j)
            for j in resp.get(Resp.DATA).get(Resp.MODELS)
        ]
    except TypeError:
        return []


def spawn_model(config: OrchestratorConfig) -> List[SpawnedModelInfo]:
    """
    Expects
    {
        "models": [
            {
                "status":  "success",
                "modelID": "1234",
                "ticker":  "PEP"
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
        for m in resp.get(Resp.MODELS):
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

    update: turns on dynamic updates

    Args:
        model_id: ID of the model to add tags to
        tags: List of tags to add to the model
        auth_token: Optional authentication token
    """

    client = new_client(auth_token)
    payload = {
        Headers.MODEL_ID: model_id,
        Headers.TAGS: tags,
        Headers.UPDATES: True,
        Headers.ROLL_FORWARD: True,
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
        LineItem from the backend, containing updated tags.

    """
    client = new_client()
    payload = {
        Headers.MODEL_ID: model_id,
        Headers.LINE_ITEM_ID: line_item_id,
        Headers.TAGS: tags
    }
    try:
        ait = client.post(
            url=VSURL.ADD_ITEM_TAGS,
            data=payload,
        )
    except ModelingServicePostException as err:
        raise TagLineItemException(
            f"error tagging line item: payload={payload} err={str(err)}")
    return LineItem.from_json(ait.get(Resp.DATA).get(Resp.LINE_ITEM))


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
    return ModelGroups.from_json(g.get(Resp.DATA))


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
                            Headers.NAME: group_name,
                            'modelIDs': model_ids
                        })
    except ModelingServicePostException as err:
        raise NewModelGroupsException(
            f"error adding new model groups: {str(err)}")
    return ModelGroups.from_json(g.get(Resp.DATA))


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

    return ModelGroups.from_json(g.get(Resp.DATA))


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
        if resp.get('status') == Vars.SUCCESS:
            if resp["data"]["models"]:
                if len(resp["data"]["models"]) > 0:
                    cases = resp["data"]["models"][0][Resp.MODEL]
            else:
                raise PullModelInformationException(
                    f"could not pull model info for model={model_id}; no models returned"
                )
        else:
            raise PullModelInformationException(
                f"could not pull model info for model={model_id}; status={resp.get('status')}"
            )

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
        headers={Headers.MODEL_ID: model_id},
    )
    return Model.from_json(resp.get(Resp.DATA).get(Resp.MODEL))


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
            f"error recalculating model: {str(err)}")

    check_success(resp,
                  'recalculating model',
                  exception=RecalculateModelException)

    return facts_list(resp.get(Resp.DATA).get(Resp.FACTS))


def remove_module(model_id: str, module_id: str):
    """Removes the specified module from the model.

    Args:
        model_id: The ID of the model.
        module_id: The ID of the module to be removed.
    """

    client = new_client()
    try:
        rm = client.post(
            url=VSURL.DELETE_MODULE,
            data={
                Headers.MODEL_ID: model_id,
                Headers.MODULE_ID: module_id,
            },
        )
    except ModelingServicePostException as err:
        raise RemoveModuleException(f'error removing module: {str(err)}')
    return rm.get('status') == Vars.SUCCESS


def rename_module(model_id: str, module_id: str,
                  new_module_name: str) -> Module:
    """Rename the module.
    
    Args:
        model_id: the ID of the model
        module_id: the ID of the module to be renamed
        new_module_name: the new name of the module.
    
    Returns:
        The new renamed module object.
    """
    client = new_client()

    r = client.post(
        url=VSURL.RENAME_MODULE,
        data={
            Headers.MODEL_ID: model_id,
            Headers.MODULE_ID: module_id,
            Headers.NAME: new_module_name
        },
    )
    check_success(r, 'adding column')
    return module_from_resp(r)


def reorder_module(model_id: str, module_id: str, line_item_id: str,
                   order: int) -> Module:
    """
    Args:
        model_id: the ID of the model
        module_id: the ID of the module
        line_item_id: the ID of the line item to be reordered
        order: the new order of the line item in the module
    
    Returns:
        The new reordered module object.
    """
    url = VSURL.REORDER_MODULE
    payload = {
        Headers.MODEL_ID: model_id,
        Headers.MODULE_ID: module_id,
        Headers.LINE_ITEM_ID: line_item_id,
        Headers.ORDER: order
    }
    c = new_client()
    r = c.post(url, data=payload)
    check_success(r, 'reorder module')
    return module_from_resp(r)


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
        line_items = resp["data"]["module"]['edges'][Resp.LINE_ITEMS]
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
    """Delete a line item from an existing module.

    Args:
        model_id: The modelID
        module_id: The ID of the module containing the line item
        line_item_id: The ID of the line item to be deleted.

    Returns:
        The `Module` without the deleted line item.
    """
    client = new_client()

    resp = client.post(
        url=VSURL.DELETE_ITEM,
        data={
            Headers.MODEL_ID: model_id,
            Headers.LINE_ITEM_ID: line_item_id,
            Headers.MODULE_ID: module_id,
        },
    )
    return module_from_resp(resp)


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
    check_success(resp, 'fact editing')
    return facts_list(resp.get(Resp.DATA).get(Resp.FACTS))


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


def edit_line_items(model_id: str,
                    line_items: List[LineItem]) -> List[LineItem]:
    """Edit line items

    The passed in line items will be used to update the line items.

    Args:
        model_id: the ID of the model containing the line items
        line_items: List of `LineItem`s that will be updated.

    """
    client = new_client()
    payload = {
        Headers.MODEL_ID: model_id,
        Headers.LINE_ITEMS: [li.jsonify() for li in line_items],
    }
    r = client.post(url=VSURL.EDIT_LINE_ITEMS, data=payload)
    check_success(r, 'line item editing')
    return line_items_list(r.get(Resp.DATA).get(Resp.LINE_ITEMS))


def add_column(model_id: str, module_id: str, new_period: float) -> Module:
    """Add a column/period to the module

    Args:
        model_id: The modelID for the module.
        module_id: The ID of the module which is to have a new column.
        new_period: The period for the new column


    Returns:
        The new `Module` object, with the new column.
    """
    url = VSURL.ADD_COLUMN
    payload = {
        Headers.MODEL_ID: model_id,
        Headers.MODULE_ID: module_id,
        Headers.NEW_PERIOD: new_period
    }
    client = new_client()
    r = client.post(url, data=payload)
    check_success(r, 'adding column')
    return module_from_resp(r)


def delete_column(model_id: str, module_id: str, period: float):
    url = VSURL.DELETE_COLUMN
    payload = {
        Headers.MODEL_ID: model_id,
        Headers.MODULE_ID: module_id,
        'period': period
    }
    client = new_client()
    r = client.post(url, data=payload)
    check_success(r, 'delete column', exception=DeleteColumnException)
    return module_from_resp(r)


def copy_model(model_id: str) -> Model:
    """Copy the model.
    
    Args:
        model_id: The modelID to be copied
    
    Returns:
        The new model.
    """
    url = VSURL.COPY_MODEL
    payload = {Headers.MODEL_ID: model_id}
    client = new_client()
    r = client.post(url, data=payload)
    check_success(r, 'copy model')
    return Model.from_json(r.get(Resp.DATA).get(Resp.MODEL))


def create_group(model_ids: List[str], group_name: str) -> GroupOfModels:
    """Create a group of models.
    
    Args:
        model_ids: List of model ids going into the group
        group_name: The name of the group
    
    Returns:
        The newly created model group object.
    """
    url = VSURL.USERS_GROUP
    payload = {Headers.NAME: group_name, Headers.MODEL_IDS: model_ids}
    client = new_client()
    r = client.post(url=url, data=payload)
    check_success(r, 'create group')
    for group in r.get(Resp.DATA):
        if group.get(Headers.NAME) == group_name:
            c = 0
            for mid in group.get(GroupOfModels.fields.MODEL_IDS):
                if mid in model_ids:
                    c += 1
                else:
                    break
            if c == len(model_ids):
                return GroupOfModels.from_json(group)
    raise Exception('group not found in response')


def execute_simulation(group_id: str, model_ids: List[str],
                       edits: List[Dict[str,
                                        str]], output_variables: List[str],
                       tag: str) -> SimulationResponse:
    """Execute a simulation for a model group.
    
    Args:
        group_id: The ID of the model group
        model_ids: The IDs of the models
        edits: List of edits to make to the target line item
        output_variables: List of names of the line items to output
        tag: Tag on the target line items
    
    Returns:
        The new simulation object.
    

    # TODO review model_ids as a required input: shouldnt be needed.
    """
    url = VSURL.SIM_SIMULATION

    ModelSimulations.validate_edits(edits)

    payload = {
        Headers.EDITS: edits,
        Headers.GROUP_ID: group_id,
        Headers.MODEL_IDS: model_ids,
        Headers.OUTPUT_VARIABLES: output_variables,
        Headers.TAG: tag
    }
    client = new_client()
    r = client.post(url=url, data=payload)
    check_success(r, 'run simulation')
    return SimulationResponse.from_json(r.get(Resp.DATA))


def simulation_output_variables(
        model_ids: List[str],
        output_variables: List[str]) -> List[ModelSimulations]:
    """ Blah

    Args:
        model_ids: list of model IDS
        output_variables: List of tags of the line items to be returned.

    Returns:
        List of model simulation objects, each with the line items (and facts) corresponding to the
        output variable tags.
    """
    url = VSURL.SIM_OUTPUT_VARIABLES
    payload = {
        Headers.MODEL_IDS: model_ids,
        Headers.OUTPUT_VARIABLES: output_variables
    }
    client = new_client()
    r = client.post(url=url, data=payload)
    check_success(r, 'simulation output variables')

    return [ModelSimulations.from_json(m) for m in r.get(Resp.DATA)]


def delete_models(model_ids: List[str]):
    """ Delete the specified models

    Args:
        model_ids: List of model IDs to be deleted.
    """
    client = new_client()
    url = VSURL.USERS_MODELS
    payload = {Headers.MODELS: model_ids}
    resp = client.delete(url=url, data=payload)
    check_success(resp, 'deleting models')
    return resp
