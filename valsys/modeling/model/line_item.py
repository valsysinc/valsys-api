from dataclasses import dataclass, field
from typing import List

# from valsys.modeling.service import edit_format, add_child_module, edit_formula
from .fact import Fact


@dataclass
class LineItem:
    uid: str
    name: str
    facts: List[Fact] = field(default_factory=list)
    tags: List[str] = None

    # def add_item(self, name, modelID, caseID):
    #    module = add_child_module(self.uid, name, modelID, caseID)
    #    return Module.from_json(module)

    # def apply_edits(self, modelID, caseID):
    #    facts = []
    #    for cell in self.facts:
    #        facts.append(
    #            {
    #                "uid": cell.uid,
    #                "formula": cell.formula,
    #                "period": cell.period,
    #                "identifier": cell.identifier,
    #            }
    #        )
    #    edit_formula(caseID, modelID, facts)

    #    print("Edit applied to:", self.name)

    # def edit_format(self, modelID, caseID):
    #    facts = []
    #    for cell in self.facts:
    #        facts.append(
    #            {"uid": cell.uid, "format": cell.fmt, "identifier": cell.identifier}
    #        )
    #    edit_format(caseID, modelID, facts)
    #    print("Format edit applied to:", self.name)

    @classmethod
    def from_json(cls, data):
        facts = []
        if data.get("facts"):
            facts = list(map(Fact.from_json, data["facts"]))
        return cls(
            uid=data["uid"], name=data["name"], facts=facts, tags=data.get("tags", None)
        )
