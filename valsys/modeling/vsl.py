from valsys.modeling.model.vsl import VSLQueryResponse, VSLSelectorsResponse
from valsys.modeling.utils import check_success
from valsys.modeling.client.service import new_client
from valsys.modeling.client.urls import VSURL
from valsys.modeling.vars import Resp, Headers
from valsys.modeling.client.exceptions import ModelingServicePostException
from valsys.modeling.vars import Resp, Vars


def execute_vsl(query):
    client = new_client()
    url = VSURL.VSL_QUERY
    payload = {
        Headers.QUERY: query,
    }

    resp = client.post(url, data=payload)
    if resp.get(Resp.STATUS) != Vars.SUCCESS:
        raise ModelingServicePostException(payload, client.status_code, url)
    return resp


def execute_vsl_query(query: str) -> VSLQueryResponse:
    """ Execute a VSL query

        Args:
            query: the VSL query string to be executed

        Returns:
            The `VSLQueryResponse` object response
    """
    resp = execute_vsl(query)
    return VSLQueryResponse.from_json(resp.get(Resp.DATA))


def execute_vsl_query_selectors(query: str) -> VSLSelectorsResponse:
    """ Execute a VSL query to return selectors

        Args:
            query: the VSL query string to be executed

        Returns:
            The `VSLSelectorsResponse` object response
    """
    resp = execute_vsl(query)
    return VSLSelectorsResponse.from_json(resp.get(Resp.DATA))
