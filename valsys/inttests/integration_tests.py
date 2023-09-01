import uuid
from typing import List
from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.inttests.runners import modeling as Runners
from valsys.inttests.runners import vsl as VSL
from valsys.inttests.utils import gen_orch_config, workflow
from valsys.utils.time import yesterday
from valsys.inttests.runners.cleanup import TestsCleanUp


def integration_test_config():

    return {
        'companyName': 'Apple',
        # 'ticker': 'PEP',
        'templateName': 'AE Template V1',
        'ticker': 'AAP US',
        # 'templateId': '9a514349-474f-48f3-8527-6f15ad5991c6',
        'numForecastYears': 3,
        'numHistoricalYears': 2,
        'industry': 'RETAIL-EATING \u0026 DRINKING PLACES',
        'startPeriod': 2019,
        'startDate': yesterday()
    }


@workflow('integration tests')
def run_integration_tests():
    cfg = integration_test_config()
    cleanup = TestsCleanUp()
    try:
        spawned_models = Runners.run_spawn_model(
            gen_orch_config(cfg=cfg, user=API_USERNAME, password=API_PASSWORD))

        model_id = spawned_models[0].model_id
        cleanup.register(Runners.run_delete_models, [model_id])
        model = Runners.run_pull_model(model_id)
        first_case_id = model.first_case_id
        first_case = model.pull_case_by_id(first_case_id)
        first_module = model.first_case.first_module
        module_id = first_module.uid
        first_line_item = first_module.line_items[0]
        first_fact = first_line_item.facts[0]

        new_module = Runners.run_add_child_module(model_id, first_case_id,
                                                  module_id)
        #Runners.run_set_facts_tracked([model_id], first_line_item.tags)
        Runners.run_recalculate_model(model_id)
        Runners.run_edit_formula(model_id, first_case_id, fact=first_fact)
        Runners.run_edit_format(model_id, first_case_id, fact=first_fact)
        tag = 't4'
        Runners.run_tag_line_item(model_id,
                                  line_item_id=first_line_item.uid,
                                  common_tag=tag)
        Runners.run_add_line_item(model_id, first_case, module_id)
        Runners.run_pull_model_information(model_id)
        Runners.run_pull_model_datasources(model_id)
        Runners.run_remove_module(model_id, new_module.uid)
        Runners.run_filter_user_model(model_id)
        Runners.run_filter_user_model_with_fields(model_id, cfg.get('ticker'))
        Runners.run_multi_filters(base_config=cfg,
                                  user=API_USERNAME,
                                  password=API_PASSWORD,
                                  cgen=gen_orch_config)
        Runners.run_delete_line_item(model_id, module_id,
                                     first_module.last_line_item.uid)
        # TODO: make this test changing the name of a different module
        # to a modules name that currently exists.
        Runners.run_rename_module(model_id, module_id, 'new name!')

        Runners.run_add_column(model_id, first_module.uid,
                               first_module.periods.pop() + 1)
        Runners.run_add_column(model_id, first_module.uid,
                               first_module.periods[0] - 1)
        Runners.run_delete_column(model_id, first_module.uid,
                                  first_module.periods[0] - 1)
        Runners.run_reorder_module(model_id, first_module.uid, first_line_item.uid,
                                   first_line_item.order + 4)
        Runners.run_recalculate_model(model_id)
        new_id = Runners.run_copy_model(model_id)
        cleanup.register(Runners.run_delete_models, [new_id])
        # Create a group constructed from the initially spawned model, and its
        # recently copied version.
        grp = Runners.run_create_group([model_id, new_id],
                                       f'new group={str(uuid.uuid1())}')

        Runners.run_execute_simulation(grp.uid,
                                       grp.model_ids,
                                       edits=[{
                                           "formula": "$FORMULA * 1.1",
                                           "timePeriod": "LFY+1"
                                       }, {
                                           "formula": "$FORMULA * 1.2",
                                           "timePeriod": "LFY-1"
                                       }],
                                       output_variables=["Net Revenue"],
                                       tag=tag,
                                       lfy=cfg['startPeriod'])
        Runners.run_simulation_output_variables(grp.model_ids, [tag])
        # find 2019 net revenue, look for sim response
        # Delete the recently created model group
        Runners.run_delete_model_group(grp.uid)
        # Deleting a group based on a deleted model should error
        Runners.run_delete_model_group(grp.uid, expect_err=True)

        # TODO: test that deleting a nonsense group ID causes an err;
        # for this to work, need to wait for updated users service.

        VSL.setup_and_run_vsl(model_id, new_id)
    except Exception:
        cleanup.run()
        raise

    # Delete the models created for testing purposes.
    cleanup.run()


@workflow('spawn simple model')
def run_spawn():

    cfg = integration_test_config()
    spawned_models = Runners.run_spawn_model(
        gen_orch_config(cfg=cfg, user=API_USERNAME, password=API_PASSWORD))

    model_id = spawned_models[0].model_id

    model = Runners.run_pull_model(model_id)
    first_case_id = model.first_case_id
    first_case = model.pull_case_by_id(first_case_id)
    first_module = model.first_case.first_module
    module_id = first_module.uid
    first_line_item = first_module.line_items[0]
    first_fact = first_line_item.facts[0]
    new_module = Runners.run_add_child_module(model_id, first_case_id,
                                              module_id)
    # Runners.run_recalculate_model(model_id)
    Runners.run_edit_formula(model_id, first_case_id, fact=first_fact)
    Runners.run_recalculate_model(model_id)
    print(model_id, cfg.get('ticker'))
