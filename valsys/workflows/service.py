import json

from valsys.spawn.models import MasterPopulateModulesConfig, ModelSpawnConfigs
from valsys.spawn.service import populate_models_with_modules, spawn_models


def main_run_spawn_models(config_file):

    spawn_config = ModelSpawnConfigs.from_json(
        config_file.get('spawnModelsConfig'))

    spawned_models = spawn_models(spawn_config, check_any=True)

    modules_config = MasterPopulateModulesConfig.from_json(
        config_file.get('populateModulesConfig'))

    populate_models_with_modules(modules_config=modules_config,
                                 spawner_report=spawned_models)

    return spawned_models


def main_run_spawn_models_from_file(config_filename: str):
    with open(config_filename, "r") as file:
        config_file = json.loads(file.read())
    return main_run_spawn_models(config_file)
