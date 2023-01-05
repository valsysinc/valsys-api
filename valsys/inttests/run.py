from valsys.utils import loggerIT as logger

from valsys.inttests.workflows import run_spawn_model, run_pull_model, run_edit_formula, run_tag_line_item, run_add_line_item, run_filter_user_models, run_pull_model_datasources, run_pull_model_information, run_remove_module, run_add_child_module, run_recalculate_model
from valsys.config.config import BASE_SCK, BASE_URL


def run_workflows():
    logger.info('running integration tests')
    logger.info(f'HTTP URL:{BASE_URL}')
    logger.info(f'SOCK URL:{BASE_SCK}')
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

    run_tag_line_item(model_id, model.first_case.first_module.line_items[0])
    run_add_line_item(model_id, first_case, module_id)
    run_pull_model_information(model_id)
    run_pull_model_datasources(model_id)
    run_remove_module(model_id, new_module.uid)
    run_filter_user_models(model_id)

    logger.info('integration tests passed ok')


if __name__ == '__main__':
    run_workflows()
