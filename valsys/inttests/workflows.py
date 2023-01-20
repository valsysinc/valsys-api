from typing import Dict, Any
from valsys.utils import loggerIT as logger
from valsys.modeling.model.case import Case
from valsys.modeling.model.fact import Fact
from valsys.modeling.model.model import Model
from valsys.inttests.utils import workflow


def workflows():
    from valsys.inttests.config import TestModelConfig
    spawned_models = run_spawn_model(TestModelConfig.MODEL)

    model_id = spawned_models[0].model_id

    model = run_pull_model(model_id)
    first_case_id = model.first_case_id
    first_case = model.pull_case_by_id(first_case_id)
    module_id = first_case.first_module.uid

    new_module = run_add_child_module(model_id, first_case_id, module_id)
    first_line_item = first_case.first_module.line_items[0]
    first_fact = first_line_item.facts[0]

    run_recalculate_model(model_id)
    run_edit_formula(model_id, first_case_id, fact=first_fact)
    run_edit_format(model_id, first_case_id, fact=first_fact)
    run_tag_line_item(model_id, line_item_id=first_line_item.uid)
    run_add_line_item(model_id, first_case, module_id)
    run_pull_model_information(model_id)
    run_pull_model_datasources(model_id)
    run_remove_module(model_id, new_module.uid)
    run_filter_user_models(model_id)
    lid = len(first_case.first_module.line_items) - 1
    run_delete_line_item(model_id, module_id,
                         first_case.first_module.line_items[lid].uid)
    #TODO: make this test changing the name of a different module
    # to a modules name that currently exists.
    run_rename_module(model_id, module_id, 'new name!')


@workflow('spawn model')
def run_spawn_model(model_config: Dict[str, Any]):
    """
    SPAWN A MODEL
    """

    # Import the spawn_model function from the modeling service
    from valsys.modeling.service import spawn_model
    from valsys.config.config import API_PASSWORD, API_USERNAME
    from valsys.seeds.loader import SeedsLoader

    # Import the class for the model seed configuration data
    from valsys.seeds.models import OrchestratorConfig, OrchestratorModelConfig
    user, password = API_USERNAME, API_PASSWORD

    template_id = SeedsLoader.template_id_by_name(
        model_config.get('templateName'))

    # Define the model seed configuration data
    model_seed_config = OrchestratorConfig(
        username=user,
        password=password,
        num_forecast_years=model_config.get('numForecastYears'),
        num_historical_years=model_config.get('numHistoricalYears'),
        start_date=model_config.get('startDate'),
        model_configs=[
            OrchestratorModelConfig(
                template_id=template_id,
                company_name=model_config.get('companyName'),
                ticker=model_config.get('ticker'),
                industry=model_config.get('industry'),
                start_period=model_config.get('startPeriod'),
            )
        ])
    # Spawn the model and obtain the new modelID
    spawned_model_id = spawn_model(model_seed_config)
    assert isinstance(spawned_model_id, list)
    return spawned_model_id


@workflow('pull model')
def run_pull_model(model_id: str) -> Model:
    from valsys.modeling.service import pull_model
    return pull_model(model_id)


@workflow('edit formula')
def run_edit_formula(model_id: str, case_id: str, fact: Fact):
    from valsys.modeling.service import edit_formula
    new_formula = '42'
    fact.formula = new_formula
    efs = edit_formula(case_id, model_id, [ff.jsonify() for ff in [fact]])
    found = False
    for f in efs:
        if f.uid == fact.uid:
            assert f.formula == new_formula
            found = True
    assert found


@workflow('edit format')
def run_edit_format(model_id: str, case_id: str, fact: Fact):
    from valsys.modeling.service import edit_format
    new_format = '{"thing":42}'
    fact.fmt = new_format
    efs = edit_format(case_id, model_id, [ff.jsonify() for ff in [fact]])
    found = False
    for f in efs:
        if f.uid == fact.uid:
            assert f.fmt == new_format
            found = True
    assert found


@workflow('tag line item')
def run_tag_line_item(model_id: str, line_item_id: str):
    from valsys.modeling.service import tag_line_item
    import uuid

    new_tags = ['t4', str(uuid.uuid1())]
    tli = tag_line_item(model_id, line_item_id, new_tags)
    assert tli.tags == new_tags


@workflow('add line item')
def run_add_line_item(model_id: str, case: Case, module_id: str):
    from valsys.modeling.service import add_line_item
    from valsys.inttests.config import AddLineItemConfig
    new_line_item_name = AddLineItemConfig.NAME
    new_line_item_order = AddLineItemConfig.ORDER
    new_line_item = add_line_item(case.uid, model_id, module_id,
                                  new_line_item_name, new_line_item_order)

    assert new_line_item.name == new_line_item_name
    assert new_line_item.order == new_line_item_order


@workflow('remove line item')
def run_delete_line_item(model_id: str, module_id: str, line_item_id: str):
    from valsys.modeling.service import delete_line_item
    from valsys.modeling.service import pull_model

    original_model = pull_model(model_id)
    original_module = original_model.pull_module(module_id)
    orig_num_line_items = len(original_module.line_items)
    original_model.pull_line_item(line_item_id)

    parent_module = delete_line_item(model_id, module_id, line_item_id)
    assert parent_module.uid == module_id
    for l in parent_module.line_items:
        assert l.uid != line_item_id
    assert len(parent_module.line_items) == orig_num_line_items - 1
    modified_model = pull_model(model_id)

    try:
        modified_model.pull_line_item(line_item_id)
    except Exception as err:
        assert "cannot find line item with id" in str(err)


@workflow('filter user models')
def run_filter_user_models(model_id: str):
    from valsys.modeling.service import filter_user_models
    found = False
    ms = filter_user_models()
    for m in ms:
        if m.uid == model_id:
            found = True
    assert found


@workflow('pull model data sources')
def run_pull_model_datasources(model_id: str):
    from valsys.modeling.service import pull_model_datasources
    ds = pull_model_datasources(model_id)
    assert isinstance(ds, str)


@workflow('pull model information')
def run_pull_model_information(model_id: str):
    from valsys.modeling.service import pull_model_information
    pull_model_information(model_id)


@workflow('add child module')
def run_add_child_module(model_id: str, case_id: str, module_id: str):
    from valsys.modeling.service import add_child_module
    new_module_name = "new Module"
    new_module = add_child_module(module_id, new_module_name, model_id,
                                  case_id)
    assert new_module.name == new_module_name
    return new_module


@workflow('remove module')
def run_remove_module(model_id: str, module_id: str):
    from valsys.modeling.service import remove_module
    from valsys.modeling.service import pull_model
    from valsys.modeling.exceptions import RemoveModuleException

    # Before we do anything, pull the model and validate
    # that the target module actually exists
    original_model = pull_model(model_id)
    original_model.pull_module(module_id)

    # Now delete the target module
    assert remove_module(model_id, module_id)

    # Now validate that the target module doesnt exist.
    m = pull_model(model_id)
    try:
        m.pull_module(module_id)
    except Exception as err:
        assert 'cannot find module with id' in str(err)

    # Just for fun, try and delete the module again;
    # it should fail.
    try:
        remove_module(model_id, module_id)
    except RemoveModuleException:
        pass


@workflow('recalculate model')
def run_recalculate_model(model_id: str):
    from valsys.modeling.service import recalculate_model
    assert recalculate_model(model_id)


@workflow('rename module')
def run_rename_module(model_id: str, module_id: str, new_name: str):
    from valsys.modeling.service import rename_module
    r = rename_module(model_id, module_id, new_name)
    assert r.get('data').get('module').get('name') == new_name
    r = rename_module(model_id, module_id, new_name)