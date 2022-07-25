import os
from pathlib import Path

from dotenv import load_dotenv

from valsys.config.env import get_envfiles
from valsys.utils.utils import read_env


BUILD = os.getenv("VALSYS_API_BUILD", 'local')
env_files = get_envfiles(BUILD)

load_dotenv(dotenv_path=Path(env_files.config))
load_dotenv(dotenv_path=Path(env_files.creds))

BASE_SCK = read_env("VALSYS_API_SOCKET")
BASE_URL = read_env("VALSYS_API_SERVER")
API_USERNAME = read_env("VALSYS_API_USER")
API_PASSWORD = read_env("VALSYS_API_PASSWORD")
