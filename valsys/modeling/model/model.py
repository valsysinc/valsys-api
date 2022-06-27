from typing import List
from .case import Case, CaseInformation
from dataclasses import dataclass, field


@dataclass
class Model(object):
    uid: str
    cases: List[Case] = field(default_factory=list)

    @classmethod
    def from_json(cls, data):
        return cls(uid=data["uid"], cases=list(map(Case.from_json, data["cases"])))

    def pull_case(self, name: str) -> Case:
        for case in self.cases:
            if case.case == name:
                return case


@dataclass
class ModelInformation:
    uid: str
    cases: List[CaseInformation] = field(default_factory=list)

    @property
    def first(self):
        if len(self.cases) == 0:
            raise ValueError("there are no cases in the model.")
        return self.cases[0]

    @classmethod
    def from_json(cls, uid, input_json):
        return cls(
            uid=uid,
            cases=list(map(CaseInformation.from_json, input_json.get("cases"))),
        )
