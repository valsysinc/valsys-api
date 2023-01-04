from typing import List, Dict, Any
from valsys.modeling.model.fact import Fact


def facts_list(facts: List[Dict[str, Any]]) -> List[Fact]:
    """Builds a list of Fact objects from a list of fact jsons."""
    return [Fact.from_json(j) for j in facts]