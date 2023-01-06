from valsys.utils import loggerIT as logger
from valsys.modeling.model.case import Case
from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.model.model import Model
from valsys.inttests.utils import workflow


@workflow('spawn model')
def run_spawn_model():
    """
    SPAWN A MODEL
    """
    from valsys.inttests.config import TestModelConfig

    # Import the spawn_model function from the modeling service
    from valsys.modeling.service import spawn_model
    from valsys.config.config import API_PASSWORD, API_USERNAME
    from valsys.seeds.loader import SeedsLoader

    # Import the class for the model seed configuration data
    from valsys.seeds.models import OrchestratorConfig, OrchestratorModelConfig
    user, password = API_USERNAME, API_PASSWORD

    template_id = SeedsLoader.template_id_by_name(
        TestModelConfig.MODEL.get('templateName'))

    # Define the model seed configuration data
    model_seed_config = OrchestratorConfig(
        username=user,
        password=password,
        num_forecast_years=TestModelConfig.MODEL.get('numForecastYears'),
        num_historical_years=TestModelConfig.MODEL.get('numHistoricalYears'),
        start_date=TestModelConfig.MODEL.get('startDate'),
        model_configs=[
            OrchestratorModelConfig(
                template_id=template_id,
                company_name=TestModelConfig.MODEL.get('companyName'),
                ticker=TestModelConfig.MODEL.get('ticker'),
                industry=TestModelConfig.MODEL.get('industry'),
                start_period=TestModelConfig.MODEL.get('startPeriod'),
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


@workflow('tag line item')
def run_tag_line_item(model_id: str, line_item: LineItem):
    from valsys.modeling.service import tag_line_item
    new_tags = ['t4']
    tli = tag_line_item(model_id, line_item.uid, new_tags)
    assert tli.tags == new_tags


@workflow('add line item')
def run_add_line_item(model_id: str, case: Case, module_id: str):
    from valsys.modeling.service import add_line_item
    new_line_item_name = 'new line item'
    new_line_item_order = 12
    new_line_item = add_line_item(case.uid, model_id, module_id,
                                  new_line_item_name, new_line_item_order)

    assert new_line_item.name == new_line_item_name
    assert new_line_item.order == new_line_item_order


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
    remove_module(model_id, module_id)


@workflow('recalculate model')
def run_recalculate_model(model_id: str):
    from valsys.modeling.service import recalculate_model
    recalculate_model(model_id)