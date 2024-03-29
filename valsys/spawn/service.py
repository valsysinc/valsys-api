import json
from typing import Any, Dict, List

from valsys.modeling.service import (
    add_child_module,
    add_line_item,
    edit_format,
    edit_formula,
    pull_model,
    pull_model_information,
)
from valsys.seeds.loader import SeedsLoader
from valsys.seeds.models import OrchestratorConfig
from valsys.spawn.models import (
    MasterPopulateModulesConfig,
    PopulateModulesConfig,
    PopulatedModules,
    SpawnProgress,
    SpawnedModels,
)
from valsys.spawn.spawn_handler import SpawnHandler
from valsys.utils import logger


class ValsysSpawn:
    """ValsysSpawn is the interface to the spawning service of models
    into the Valsys platform."""

    @staticmethod
    def spawn_models(config):
        try:
            return spawn_models(config)
        except Exception as err:
            logger.exception(err)
        return None

    @staticmethod
    def populate_modules(config: PopulateModulesConfig):
        return populate_modules(config)


def spawn_models_same_template_periods(
        model_spawn_config: OrchestratorConfig) -> List[SpawnProgress]:
    """
    Spawn a set of models, each of which has the same 
    - template name,
    - proj period, 
    - hist period,
    - email list to share to
    - tags
    """

    tickers = model_spawn_config.tickers

    logger.info(f"running spawn with {model_spawn_config.tickers}")

    company_configs = SeedsLoader.company_configs_by_ticker(tickers)

    template_id = SeedsLoader.template_id_by_name(
        template_name=model_spawn_config.template_name)

    for config in model_spawn_config.model_configs:
        config.update(company_configs[config.ticker])
        config.template_id = template_id

    return SpawnHandler.orchestrate_model_spawns(seeds=model_spawn_config)


def spawn_models(configs: List[OrchestratorConfig],
                 check_any=False) -> SpawnedModels:
    """Spawn models from the provided configuration.

    If `check_any` is `True`, then a `ValueError` is raised if no models
    have been spawned.
    `check_any` is False by default.
    """
    rep = SpawnedModels(verbose=True)
    for cfg in configs:
        [rep.append(proc) for proc in spawn_models_same_template_periods(cfg)]

    if check_any and len(rep.spawned_models) == 0:
        raise ValueError(f"no models spawned")

    return rep


def spawn_from_config(seed_config: Dict[str, Any]):
    model_seed_config = OrchestratorConfig.from_json(seed_config)

    # Spawn the model and obtain the new modelID
    return spawn_models([model_seed_config])


def orchestrate_model_spawns(orchestrator_configuration: OrchestratorConfig):
    return SpawnHandler.orchestrate_model_spawns(orchestrator_configuration)


def populate_models_with_modules(
        modules_config: MasterPopulateModulesConfig,
        spawner_report: SpawnedModels) -> SpawnedModels:

    for pmc in modules_config:
        model_ids_for_tickers = spawner_report.spawned_model_ids_for_tickers(
            pmc.tickers)
        pmc.set_model_ids(model_ids_for_tickers)
        pmc_rep = populate_modules(pmc)

        spawner_report.add_populated_modules(pmc_rep)

    #logger.info(spawner_report)
    return spawner_report


def populate_modules(config: PopulateModulesConfig) -> PopulatedModules:
    """All models in the config are populated
    with the same module data (i.e., module names, line items per module,
    and formulae per fact.)"""
    model_ids = config.model_ids
    key_metrics_config = config.key_metrics_config

    populated_modules_report = PopulatedModules()
    for model_id in model_ids:

        model_info = pull_model_information(model_id)

        case_id = model_info.first.uid
        model = pull_model(model_id)

        case = model.pull_case_by_id(case_id=case_id)
        populated_modules_report.add_model(model_id, case.case)
        root_module = case.pull_module(config.parent_module_name)

        # Create module
        module_name = config.module_name
        new_module = add_child_module(parent_module_id=root_module.uid,
                                      name=module_name,
                                      model_id=model_id,
                                      case_id=case_id)
        new_module_id = new_module.uid
        populated_modules_report.add_module_to_model(
            model_id=model_id,
            module_id=new_module_id,
            name=module_name,
            uid_parent=root_module.uid)
        line_item_data = config.line_item_data
        key_metrics = key_metrics_config.get('metrics')
        key_metrics_format = json.dumps(key_metrics_config.get('format'))

        for li in line_item_data:
            item_name = li.name
            line_item = add_line_item(case_id=case_id,
                                      model_id=model_id,
                                      module_id=new_module_id,
                                      name=item_name,
                                      order=li.order)

            populated_modules_report.add_line_item_to_module(
                model_id=model_id,
                module_id=new_module_id,
                line_item_uid=line_item.uid,
                line_item_name=line_item.name)

            if item_name in key_metrics:
                for idx, cell in enumerate(line_item.facts):
                    cell.fmt = key_metrics_format
                    line_item.facts[idx] = cell
                edit_format(case_id=case_id,
                            model_id=model_id,
                            facts=line_item.facts_for_format_edit())
                populated_modules_report.add_process_to_line_item(
                    model_id=model_id,
                    module_id=new_module_id,
                    line_item_uid=line_item.uid,
                    proc_name='EDIT_FORMAT')

            formula_edits = config.get_line_item_config(
                line_item.name).formula_edits
            if len(formula_edits) == 0:
                continue

            for idx, cell in enumerate(line_item.facts):
                for e in formula_edits:
                    if cell.period == int(e.period_year):
                        cell.formula = e.formula
                line_item.replace_fact(idx, cell)

            edit_formula(case_id, model_id, line_item.facts_for_formula_edit())

            populated_modules_report.add_process_to_line_item(
                model_id=model_id,
                module_id=new_module_id,
                line_item_uid=line_item.uid,
                proc_name='EDIT_FORMULA')
    return populated_modules_report
