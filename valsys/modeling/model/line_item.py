from dataclasses import dataclass, field
from typing import List

from .fact import Fact


@dataclass
class LineItem:
    uid: str
    name: str
    facts: List[Fact] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    class fields:
        UID = 'id'
        NAME = 'name'
        ORDER = 'order'
        TAGS = 'tags'
        EDGES = 'edges'
        FACTS = 'facts'

    def jsonify_facts(self, fields=None):
        return [f.jsonify(fields) for f in self.facts]

    def replace_fact(self, idx, new_fact: Fact):
        self.facts[idx] = new_fact

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
        return cls(uid=data[cls.fields.UID],
                   name=data[cls.fields.NAME],
                   facts=list(
                       map(
                           Fact.from_json,
                           data.get(cls.fields.EDGES,
                                    {}).get(cls.fields.FACTS, []))),
                   tags=data.get(cls.fields.TAGS, []))

    def jsonify(self):
        return {
            self.fields.UID: self.uid,
            self.fields.NAME: self.name,
            self.fields.EDGES: {
                self.fields.FACTS: [f.jsonify() for f in self.facts]
            },
            self.fields.TAGS: self.tags
        }