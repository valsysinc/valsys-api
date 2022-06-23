import json
import requests
from typing import Dict, List, Any
from valsys.config import API_PASSWORD, API_USERNAME
from valsys.auth.service import authenticate
from valsys.spawn.socket_handler import SocketHandler
from valsys.utils import logger
from valsys.spawn.models import ModelSeedConfigurationData

auth_token = authenticate(username=API_USERNAME, password=API_PASSWORD)


def load_company_configs(n: int = 5) -> List[Dict[str, str]]:
    URL_CONFIGURATION = "http://localhost:8080/configuration"
    configs = requests.post(url=URL_CONFIGURATION, data=json.dumps({}))

    return json.loads(configs.content).get("data").get("data")[:n]


hist_period, proj_period = 5, 11

configs = load_company_configs(n=2)
config = configs[0]

mscd = ModelSeedConfigurationData.from_api(
    config, proj_period=proj_period, hist_period=hist_period
)
mscd.pp()

sh = SocketHandler(config=mscd.jsonify(), auth_token=auth_token, trace=True)
sh.run()

while True:
    if sh.state != "COMPLETE":
        continue
    if sh.error is not None:
        print("error building model:", sh.error)
    break
