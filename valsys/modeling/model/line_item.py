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

    def jsonify_facts(self, fields=None):
        return [f.jsonify(fields) for f in self.facts]

    # def add_item(self, name, modelID, caseID):
    #    module = add_child_module(self.uid, name, modelID, caseID)
    #    return Module.from_json(module)

    def facts_for_formula_edit(self):
        return self.jsonify_facts(fields=[
            Fact.fields.UID, Fact.fields.FORMULA, Fact.fields.PERIOD,
            Fact.fields.IDENTIFIER
        ])

    def facts_for_format_edit(self):
        return self.jsonify_facts(fields=[
            Fact.fields.UID, Fact.fields.IDENTIFIER, Fact.fields.FORMAT
        ])

    @classmethod
    def from_json(cls, data):
        facts = []
        if data.get("facts"):
            facts = list(map(Fact.from_json, data["facts"]))
        return cls(uid=data["uid"],
                   name=data["name"],
                   facts=facts,
                   tags=data.get("tags", None))
