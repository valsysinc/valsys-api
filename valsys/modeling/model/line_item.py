from dataclasses import dataclass, field
from typing import List

from .fact import Fact


@dataclass
class LineItem:
    uid: str
    name: str
    facts: List[Fact] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    order: int = 1

    class fields:
        ID = 'id'
        NAME = 'name'
        TAGS = 'tags'
        EDGES = 'edges'
        FACTS = 'facts'
        ORDER = 'order'

    def pull_fact_by_identifier(self, fact_identifier: str) -> Fact:
        """Extract a fact from the line item, by matching its
        identifier with the target.
        
        A fact identifier is a string usually of the form
        [MODULE[LINEITEM[YEAR]]].
        """
        for fact in self.facts:
            if fact.identifier == fact_identifier:
                return fact
        return None

    def pull_fact_by_id(self, fact_id: str):
        for fact in self.facts:
            if fact.uid == fact_id:
                return fact
        return None

    def jsonify_facts(self, fields=None):
        return [f.jsonify(fields) for f in self.facts]

    def replace_fact(self, idx: int, new_fact: Fact):
        try:
            self.facts[idx] = new_fact
        except IndexError:
            raise Exception(
                f"tried to replace fact at index {idx}; does not exist in facts list"
            )

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
        return cls(uid=data[cls.fields.ID],
                   name=data[cls.fields.NAME],
                   facts=list(
                       map(
                           Fact.from_json,
                           data.get(cls.fields.EDGES,
                                    {}).get(cls.fields.FACTS, []))),
                   tags=data.get(cls.fields.TAGS, []),
                   order=data.get(cls.fields.ORDER, ''))
