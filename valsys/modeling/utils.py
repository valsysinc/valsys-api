from typing import Any, Dict, List, Protocol

from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.vars import Vars


class Deserialiseable(Protocol):

    def from_json(self, d: List[Dict[str, Any]]):
        ...


def from_list(m: Deserialiseable, d: List[Dict[str, Any]]):
    return [m.from_json(j) for j in d]


def facts_list(facts: List[Dict[str, Any]]) -> List[Fact]:
    """Builds a list of Fact objects from a list of fact jsons."""
    return from_list(Fact, facts)


def line_items_list(line_items: List[Dict[str, Any]]) -> List[LineItem]:
    """Builds a list of Line Item objects from a list of line item jsons."""
    return from_list(LineItem, line_items)


def check_success(resp, desc, exception=Exception):
    if resp.get('status') != Vars.SUCCESS:
        raise exception(f'{desc} failed {resp.get("error")}')
    return True