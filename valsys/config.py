import os
from dotenv import load_dotenv
from pathlib import Path
from valsys.utils.utils import read_env

BUILD = os.getenv("VALSYS_API_BUILD", 'test')
if BUILD == 'test':
    print('VALSYS_API_BUILD=test')
    load_dotenv(dotenv_path=Path('env/.env.test'))
else:
    load_dotenv(dotenv_path=Path('env/.env'))

BASE_SCK = "ws://localhost:5100"
BASE_URL = read_env("VALSYS_API_SERVER")
API_USERNAME = read_env("VALSYS_API_USER")
API_PASSWORD = read_env("VALSYS_API_PASSWORD")
