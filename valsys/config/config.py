import os
from pathlib import Path

from dotenv import load_dotenv

from valsys.config.env import get_envfiles
from valsys.utils.utils import read_env


def load_from_env_file(build: str):
    env_files = get_envfiles(build)
    load_dotenv(dotenv_path=Path(env_files.config))
    load_dotenv(dotenv_path=Path(env_files.creds))


_BUILD = os.getenv("VALSYS_API_BUILD", 'local')
if _BUILD in ['local', 'test']:
    load_from_env_file(_BUILD)
else:
    print(f"BUILD={_BUILD}")
BASE_SCK = read_env("VALSYS_API_SOCKET")
BASE_URL = read_env("VALSYS_API_SERVER")
API_USERNAME = read_env("VALSYS_API_USER")
API_PASSWORD = read_env("VALSYS_API_PASSWORD")
