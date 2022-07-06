import sys
import json
import pyfiglet
from valsys.spawn.service import spawn_models, populate_modules
from valsys.version import VERSION, NAME
from valsys.utils import logger
from valsys.spawn.models import PopulateModulesConfig, ModelSpawnConfig


def run_spawn_models(args):
    config_filename = args[0]
    with open(config_filename, "r") as file:
        config_file = json.loads(file.read())
    spawn_config = ModelSpawnConfig.from_json(config_file.get('spawnModelsConfig'))
    spawner_report = spawn_models(spawn_config)

    pmc = PopulateModulesConfig.from_json(model_ids=spawner_report.spawned_model_ids,
                                          config=config_file.get('populateModulesConfig')[0])
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
