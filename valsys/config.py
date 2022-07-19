import os
from pathlib import Path

from dotenv import load_dotenv

from valsys.utils.utils import read_env


BUILD = os.getenv("VALSYS_API_BUILD", 'local')
if BUILD == 'test':
    print('VALSYS_API_BUILD=test')
    load_dotenv(dotenv_path=Path('env/.env.test'))
else:
    load_dotenv(dotenv_path=Path('env/.env'))

BASE_SCK = read_env("VALSYS_API_SOCKET")
BASE_URL = read_env("VALSYS_API_SERVER")
API_USERNAME = read_env("VALSYS_API_USER")
API_PASSWORD = read_env("VALSYS_API_PASSWORD")
