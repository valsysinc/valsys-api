from dataclasses import dataclass, field
from typing import Any, Dict, List

from .case import Case, CaseInformation


@dataclass
class Model(object):
    uid: str
    styling: str
    cases: List[Case] = field(default_factory=list)

    class fields:
        UID = 'id'
        STYLING = 'styling'
        TITLE = 'title'
        CASES = 'cases'
        EDGES = 'edges'

    @classmethod
    def from_json(cls, data):
        return cls(uid=data[cls.fields.UID],
                   styling=data.get(cls.fields.STYLING),
                   cases=list(
                       map(
                           Case.from_json,
                           data.get(cls.fields.EDGES,
                                    {}).get(cls.fields.CASES))))

    def pull_case(self, name: str) -> Case:
        for case in self.cases:
            if case.case == name:
                return case


@dataclass
class ModelInformation:
    # TODO: combine with  datastructure `ModelDetailInformation` in valsys.modeling.models
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
    def from_json(cls, uid: str, input_json: Dict[str, Any]):

        tags = input_json.get(cls.fields.TAGS, '').split(',')
        return cls(uid=uid,
                   tags=[t for t in tags if t],
                   cases=list(
                       map(CaseInformation.from_json,
                           input_json.get(cls.fields.CASES, []))),
                   data_sources=input_json.get(cls.fields.DATA_SOURCES, ''))
