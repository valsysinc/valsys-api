import sys
import json
import pyfiglet
from valsys.spawn.service import spawn_models, populate_modules
from valsys.version import VERSION, NAME
from valsys.utils import logger
from valsys.spawn.models import ModelSpawnConfig, MasterPopulateModulesConfig


def run_spawn_models(args):
    config_filename = args[0]
    with open(config_filename, "r") as file:
        config_file = json.loads(file.read())
    spawn_config = ModelSpawnConfig.from_json(config_file.get('spawnModelsConfig'))
    spawner_report = spawn_models(spawn_config)
    spawned_models = spawner_report.spawned_models

    if len(spawned_models) == 0:
        raise ValueError(f"no models spawned")
    mpmc = MasterPopulateModulesConfig.from_json(config_file.get('populateModulesConfig'))
    for pmc in mpmc:
        model_ids_for_ticker = spawner_report.spawned_model_ids_for_tickers(pmc.tickers)
        pmc.set_model_ids(model_ids_for_ticker)
        populate_modules(pmc)
    return spawner_report


def main(args):
    print(pyfiglet.figlet_format(NAME), f"{' '*10} v{VERSION}")
    logger.info(f"start")
    res = run_spawn_models(args)
    if res.has_errors:
        logger.info(f'done with errors')
    else:
        logger.info(f'done')


if __name__ == "__main__":
    main(sys.argv[1:])
