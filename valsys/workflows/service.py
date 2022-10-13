import json
import datetime

from valsys.seeds.models import OrchestratorConfig
from valsys.spawn.models import MasterPopulateModulesConfig
from valsys.spawn.service import populate_models_with_modules, spawn_models
from valsys.modeling.service import create_model
from valsys.seeds.loader import SeedsLoader
from valsys.seeds.models import DATETIME_FORMAT


def run_spawn_models(config_file):

    spawn_configs = [
        OrchestratorConfig.from_json(sm)
        for sm in config_file.get('spawnModelsConfig')
    ]

    spawned_models = spawn_models(spawn_configs, check_any=True)

    modules_config = MasterPopulateModulesConfig.from_json(
        config_file.get('populateModulesConfig'))

    populate_models_with_modules(modules_config=modules_config,
                                 spawner_report=spawned_models)

    return spawned_models


def run_spawn_models_from_file(config_filename: str):
    with open(config_filename, "r") as file:
        config_file = json.loads(file.read())
    return run_spawn_models(config_file)


def generate_model_from_file(config_filename: str):
    with open(config_filename, "r") as file:
        config_file = json.loads(file.read())
    cfgs = []
    for b in config_file:
        tid = SeedsLoader.template_id_by_name(b.get('templateName'))
        cinfo = SeedsLoader.company_configs_by_ticker(
            [t['ticker'] for t in b['tickers']])
        nfy = b.get('numForecastYears')
        nhy = b.get('numHistoricalYears')
        for t in b.get('tickers'):
            tkr = t['ticker']
            ti = cinfo[tkr]
            cfg = {
                "action": "CREATE_MODEL",
                "companyName": ti.company_name,
                "currency": ti.currency,
                "geography": ti.geography,
                "industry": ti.industry,
                "numForecastYears": nfy,
                "numHistoricalYears": nhy,
                "periodType": "ANNUAL",
                "companyType": "Public",
                "startDate": datetime.datetime.now().strftime(DATETIME_FORMAT),
                "startPeriod": ti.start_period,
                "templateID": tid,
                "ticker": tkr,
                "title": tkr + " - 06/02/2022",
            }
            cfgs.append(cfg)

    for cfg in cfgs:
        create_model(cfg)
        print(f"generated model {cfg['ticker']}")