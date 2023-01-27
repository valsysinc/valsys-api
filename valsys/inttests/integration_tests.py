import datetime

from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.inttests.runners import runners as Runners
from valsys.inttests.utils import gen_orch_config, workflow


def integration_test_config():
    sd = (datetime.datetime.utcnow() -
          datetime.timedelta(days=1)).isoformat() + "Z"
    return {
        'companyName': 'Pepsi',
        'ticker': 'PEP',
        'templateName': 'dcf-standard',
        'numForecastYears': 3,
        'numHistoricalYears': 2,
        'industry': 'RETAIL-EATING \u0026 DRINKING PLACES',
        'startPeriod': 2019,
        'startDate': sd
    }


@workflow('integration tests')
def run_integration_tests():

    spawned_models = Runners.run_spawn_model(
        gen_orch_config(integration_test_config(), API_USERNAME, API_PASSWORD))

    model_id = spawned_models[0].model_id

    model = Runners.run_pull_model(model_id)
    first_case_id = model.first_case_id
    first_case = model.pull_case_by_id(first_case_id)
    module_id = first_case.first_module.uid

    new_module = Runners.run_add_child_module(model_id, first_case_id,
                                              module_id)
    first_line_item = first_case.first_module.line_items[0]
    first_fact = first_line_item.facts[0]

    Runners.run_recalculate_model(model_id)
    Runners.run_edit_formula(model_id, first_case_id, fact=first_fact)
    Runners.run_edit_format(model_id, first_case_id, fact=first_fact)
    Runners.run_tag_line_item(model_id, line_item_id=first_line_item.uid)
    Runners.run_add_line_item(model_id, first_case, module_id)
    Runners.run_pull_model_information(model_id)
    Runners.run_pull_model_datasources(model_id)
    Runners.run_remove_module(model_id, new_module.uid)
    Runners.run_filter_user_models(model_id)
    Runners.run_delete_line_item(model_id, module_id,
                                 first_case.first_module.last_line_item.uid)
    #TODO: make this test changing the name of a different module
    # to a modules name that currently exists.
    Runners.run_rename_module(model_id, module_id, 'new name!')
    m = model.first_case.first_module
    Runners.run_add_column(model_id, m.uid, m.periods.pop() + 1)
    Runners.run_add_column(model_id, m.uid, m.periods[0] - 1)
