from typing import List
from .case import Case
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
