from valsys.utils import loggerIT as logger

from valsys.inttests.workflows import run_spawn_model, run_pull_model, run_edit_formula
from valsys.inttests.workflows import run_tag_line_item, run_add_line_item, run_filter_user_models
from valsys.inttests.workflows import run_pull_model_datasources, run_pull_model_information, run_remove_module
from valsys.inttests.workflows import run_add_child_module, run_recalculate_model, run_edit_format, run_delete_line_item
from valsys.inttests.workflows import run_rename_module
from valsys.config.config import BASE_SCK, BASE_URL


def run_workflows():
    logger.info('running integration tests')
    logger.info(f'modeling service HTTP URL:{BASE_URL}')
    logger.info(f'modeling service SOCK URL:{BASE_SCK}')

    spawned_models = run_spawn_model()
    model_id = spawned_models[0].model_id

    model = run_pull_model(model_id)
    first_case_id = model.first_case_id
    first_case = model.pull_case_by_id(first_case_id)
    module_id = first_case.first_module.uid

    new_module = run_add_child_module(model_id, first_case_id, module_id)

    run_recalculate_model(model_id)
    run_edit_formula(model_id,
                     first_case_id,
                     fact=model.first_case.first_module.line_items[0].facts[0])
    run_edit_format(model_id,
                    first_case_id,
                    fact=model.first_case.first_module.line_items[0].facts[0])
    run_tag_line_item(
        model_id, line_item_id=model.first_case.first_module.line_items[0].uid)
    run_add_line_item(model_id, first_case, module_id)
    run_pull_model_information(model_id)
    run_pull_model_datasources(model_id)
    run_remove_module(model_id, new_module.uid)
    run_filter_user_models(model_id)
    lid = len(model.first_case.first_module.line_items) - 1
    run_delete_line_item(model_id, module_id,
                         model.first_case.first_module.line_items[lid].uid)
    #TODO: make this test changing the name of a different module
    # to a modules name that currently exists.
    run_rename_module(model_id, module_id, 'new name!')
    logger.info('integration tests passed ok')
