from typing import List, Dict

import json
import requests
from valsys.config import URL_CONFIGS, URL_TEMPLATES


def load_company_configs(count: int = 5) -> List[Dict[str, str]]:
    """Load and return `n` company configurations from the Valsys
    `uploader` API."""
    resp = requests.post(url=URL_CONFIGS, data=json.dumps({}))
    return json.loads(resp.content).get("data").get("data")[:count]


def load_templates(auth_token):
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + auth_token,
    }
    resp = requests.get(url=URL_TEMPLATES, headers=headers)
    return json.loads(resp.content).get("data")
