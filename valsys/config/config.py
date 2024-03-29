import os
from pathlib import Path

from dotenv import load_dotenv

from valsys.config.env import get_envfiles
from valsys.utils.utils import read_env


BUILDS_TO_LOAD_FROM_ENV_FILES = ['local', 'test']


def load_from_env_file(build: str):
    env_files = get_envfiles(build)
    load_dotenv(dotenv_path=Path(env_files.config))
    load_dotenv(dotenv_path=Path(env_files.creds))


def get_build():
    return os.getenv("VALSYS_API_BUILD", '')


_BUILD = get_build()
if _BUILD in BUILDS_TO_LOAD_FROM_ENV_FILES:
    load_from_env_file(_BUILD)
else:
    print(f"BUILD={_BUILD}")

BASE_SCK = read_env("VALSYS_API_SOCKET")
BASE_ORCH = read_env("VALSYS_API_SOCKET_ORCH", required=False)
BASE_URL = read_env("VALSYS_API_SERVER")
API_USERNAME = read_env("VALSYS_API_USER")
API_PASSWORD = read_env("VALSYS_API_PASSWORD")
HOST = read_env('HOST', required=False)
if BASE_ORCH is None:
    BASE_ORCH = BASE_SCK

# BASE_SCK -> create ws://modeling:5100
# BASE_ORCH -> /orchestrator/connect/ ->


def log_modeling_service_info(logger):
    logger(f'modeling service HTTP URL:{BASE_URL}')
    logger(f'modeling service SOCK URL:{BASE_SCK}')
