from typing import Any, Dict, List, Protocol

from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.model.module import Module
from valsys.modeling.vars import Resp, Vars


class Deserialiseable(Protocol):

    def from_json(self, d: List[Dict[str, Any]]):
        ...


def module_from_resp(r):
    return Module.from_json(r.get(Resp.DATA).get(Resp.MODULE))


def from_list(m: Deserialiseable, d: List[Dict[str, Any]]):
    return [m.from_json(j) for j in d]


def facts_list(facts: List[Dict[str, Any]]) -> List[Fact]:
    """Builds a list of Fact objects from a list of fact jsons."""
    return from_list(Fact, facts)


def line_items_list(line_items: List[Dict[str, Any]]) -> List[LineItem]:
    """Builds a list of Line Item objects from a list of line item jsons."""
    return from_list(LineItem, line_items)


def check_success(resp: Dict[str, Any],
                  desc: str,
                  exception: Exception = Exception):
    '''Check to see if the supplied response dict has
    a successful status.
    
    If not "success", then an exception is raised along with the provided description
    for context. Custom exception classes can be pased in.'''
    if resp.get(Resp.STATUS) != Vars.SUCCESS:
        raise exception(f'{desc} failed {resp.get(Resp.ERROR)}')
    return True
