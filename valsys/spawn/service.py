import datetime
from multiprocessing.context import SpawnProcess
from typing import List
import json
from valsys.utils import logger
from valsys.seeds.loader import SeedsLoader
from valsys.seeds.models import ModelSeedConfigurationData
from valsys.spawn.spawn_handler import SpawnHandler
from valsys.spawn.models import PopulateModulesConfig, ModelSpawnConfig, ModelSpawnConfigs
from valsys.modeling.service import edit_format, edit_formula, pull_case, pull_model_information, add_item, add_child_module
from valsys.spawn.models import (
    SpawnerProgress, SpawnProgress
)


class ValsysSpawn:
    """ValsysSpawn is the interface to the spawning service of models
    into the Valsys platform."""
    @staticmethod
    def spawn_models(config: ModelSpawnConfig):
        try:
            return spawn_models(config)
        except Exception as err:
            logger.exception(err)

    @staticmethod
    def populate_modules(config: PopulateModulesConfig):
        return populate_modules(config)


def spawn_models_same_dcf_periods(config: ModelSpawnConfig) -> List[SpawnProgress]:

    tickers = config.tickers
    template_name = config.template_name
    proj_period = config.proj_period
    hist_period = config.hist_period
    tags = config.tags
    emails = config.emails

    logger.info(f"running spawn with {config.jsonify()}")

    company_configs = SeedsLoader.company_configs_by_ticker(tickers)
    template_id = SeedsLoader.template_id_by_name(template_name=template_name)

    seeds: List[ModelSeedConfigurationData] = []
    for config in company_configs:
        seeds.append(
            ModelSeedConfigurationData(
                company_name=config.company_name,
                ticker=config.ticker,
                industry_group=config.industry,
                start_period=config.start_period,
                start_date=datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"),
                proj_period=proj_period,
                hist_period=hist_period,
                template_id=template_id,
            ))

    return SpawnHandler.build_and_spawn_models(
        seeds=seeds,
        tags=tags,
        emails=emails,
    )


def spawn_models(configs: ModelSpawnConfigs) -> SpawnerProgress:
    rep = SpawnerProgress()
    for cfg in configs:
        [rep.append(proc) for proc in spawn_models_same_dcf_periods(cfg)]
    return rep


def populate_modules(config: PopulateModulesConfig):

    model_ids = config.model_ids
    parent_module_name = config.parent_module_name
    module_name = config.module_name
    key_metrics_config = config.key_metrics_config
    line_item_data = config.line_item_data

    key_metrics = key_metrics_config.get('metrics')
    key_metrics_format = json.dumps(key_metrics_config.get('format'))

    for model_id in model_ids:

        # Pull the first case uid
        model_info = pull_model_information(model_id)

        case_id = model_info.first.uid
        case = pull_case(uid=case_id)

        root_module = case.pull_module(parent_module_name)

        # Create module
        new_module = add_child_module(parent_module_id=root_module.uid,
                                      name=module_name,
                                      model_id=model_id,
                                      case_id=case_id)
        new_module_id = new_module.uid
        for li in line_item_data:
            item_name = li.name
            line_item = add_item(case_id=case_id,
                                 model_id=model_id,
                                 name=item_name,
                                 order=li.order,
                                 module_id=new_module_id)
            if item_name in key_metrics:
                for idx, cell in enumerate(line_item.facts):
                    cell.fmt = key_metrics_format
                    line_item.facts[idx] = cell
                edit_format(case_id=case_id,
                            model_id=model_id,
                            facts=line_item.facts_for_format_edit())

            formula_edits = config.get_line_item_config(line_item.name).formula_edits
            if len(formula_edits) == 0:
                continue
            for idx, cell in enumerate(line_item.facts):
                for e in formula_edits:
                    if cell.period == int(e.period_year):
                        cell.formula = e.formula
                line_item.replace_fact(idx, cell)
            edit_formula(case_id, model_id, line_item.facts_for_formula_edit())
