import json
import sys

import pyfiglet

from valsys.spawn.models import MasterPopulateModulesConfig, ModelSpawnConfigs
from valsys.spawn.service import spawn_models, populate_models_with_modules
from valsys.utils import logger
from valsys.version import NAME, VERSION


def run_spawn_models(args):
    config_filename = args[0]
    with open(config_filename, "r") as file:
        config_file = json.loads(file.read())

    spawn_config = ModelSpawnConfigs.from_json(
        config_file.get('spawnModelsConfig'))

    spawned_models = spawn_models(spawn_config, check_any=True)

    modules_config = MasterPopulateModulesConfig.from_json(
        config_file.get('populateModulesConfig'))

    populate_models_with_modules(modules_config=modules_config,
                                 spawner_report=spawned_models)

    return spawned_models


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
