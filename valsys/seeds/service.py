from typing import List, Dict
from valsys.modeling.client.urls import VSURL
from valsys.modeling.service import new_client


def load_company_configs() -> List[Dict[str, str]]:
    """Load and return company configurations from the Valsys
    `uploader` API."""
    client = new_client()
    resp = client.post(url=VSURL.CONFIGS)
    return resp.json().get("data").get("data")


def load_templates():
    """Load all templates"""
    client = new_client()
    resp = client.get(url=VSURL.TEMPLATES)
    return resp.get("data")
