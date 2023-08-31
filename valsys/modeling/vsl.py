from valsys.modeling.model.vsl import VSLQueryResponse, VSLSelectorsResponse
from valsys.modeling.utils import (
    check_success,

)
from valsys.modeling.client.service import new_client
from valsys.modeling.client.urls import VSURL
from valsys.modeling.vars import Resp, Headers


def execute_vsl_query(query: str) -> VSLQueryResponse:
    client = new_client()
    url = VSURL.VSL_QUERY
    payload = {
        Headers.QUERY: query,
    }
    resp = client.post(url, data=payload)
    check_success(resp, 'VSL query')
    return VSLQueryResponse.from_json(resp.get(Resp.DATA))


def execute_vsl_query_selectors(query: str) -> VSLSelectorsResponse:
    client = new_client()
    url = VSURL.VSL_QUERY
    payload = {
        Headers.QUERY: query,
    }
    resp = client.post(url, data=payload)
    check_success(resp, 'VSL query selectors')
    return VSLSelectorsResponse.from_json(resp.get(Resp.DATA))
