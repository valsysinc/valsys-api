from typing import List, Dict
from valsys.config import API_PASSWORD, API_USERNAME, URL_CONFIGS, URL_TEMPLATES
from valsys.auth import authenticate

import json
import requests


def load_company_configs() -> List[Dict[str, str]]:
    """Load and return `n` company configurations from the Valsys
    `uploader` API."""
    resp = requests.post(url=URL_CONFIGS, data=json.dumps({}))
    return json.loads(resp.content).get("data").get("data")


def load_templates():
    """Load all templates"""
    auth_token = authenticate(username=API_USERNAME, password=API_PASSWORD)

    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + auth_token,
    }
    resp = requests.get(url=URL_TEMPLATES, headers=headers)
    return json.loads(resp.content).get("data")


def load_template_id_by_name(template_name: str) -> str:
    """Load the template ID by the template name."""
    templates = load_templates()
    for template in templates:
        if template.get("template_name") == template_name:
            return template.get("uid")
    raise ValueError(f"template not found for template_name: {template_name}")


def load_company_configs_by_ticker(tickers: List[str]):
    ret = []
    configs = load_company_configs()
    for cfg in configs:
        if cfg.get("ticker") in tickers:
            ret.append(cfg)
    return ret
