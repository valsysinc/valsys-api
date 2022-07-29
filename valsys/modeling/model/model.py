from dataclasses import dataclass, field
from typing import List

from .case import Case, CaseInformation


@dataclass
class Model(object):
    uid: str
    cases: List[Case] = field(default_factory=list)

    @classmethod
    def from_json(cls, data):
        return cls(uid=data["uid"],
                   cases=list(map(Case.from_json, data["cases"])))

    def pull_case(self, name: str) -> Case:
        for case in self.cases:
            if case.case == name:
                return case


@dataclass
class ModelInformation:

    uid: str
    tags: List[str] = field(default_factory=list)
    cases: List[CaseInformation] = field(default_factory=list)
    data_sources: str = ''

    class fields:
        TAGS = 'modelTags'
        CASES = 'cases'
        DATA_SOURCES = 'dataSources'

    @property
    def case_id(self):
        return self.first.uid

    @property
    def first(self):
        if len(self.cases) == 0:
            raise ValueError("there are no cases in the model.")
        return self.cases[0]

    @classmethod
    def from_json(cls, uid, input_json):

        tags = input_json.get(cls.fields.TAGS, '').split(',')
        return cls(uid=uid,
                   tags=[t for t in tags if t],
                   cases=list(
                       map(CaseInformation.from_json,
                           input_json.get(cls.fields.CASES, []))),
                   data_sources=input_json.get(cls.fields.DATA_SOURCES, ''))
