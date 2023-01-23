from dataclasses import dataclass, field
from typing import Any, Dict, List

from .case import Case, CaseInformation


@dataclass
class Model(object):
    uid: str
    cases: List[Case] = field(default_factory=list)

    class fields:
        ID = 'id'
        EDGES = 'edges'
        CASES = 'cases'

    def pull_case(self, name: str) -> Case:
        for case in self.cases:
            if case.case == name:
                return case

    def pull_module(self, module_id: str):
        """Extract a module by ID from the model.
        
        Note that the first module with the given id will be returned.
        """
        for case in self.cases:
            for module in case.modules:

                if module.uid == module_id:
                    return module
                for cm in module.child_modules:
                    if cm.uid == module_id:
                        return cm
        raise Exception(f'cannot find module with id {module_id}')

    def pull_module_by_name(self, module_name: str):
        for case in self.cases:
            try:
                return case.pull_module(module_name)
            except ValueError:
                pass
        raise Exception(f'cannot find module with name {module_name}')

    def pull_line_item(self, line_item_id: str):
        """Extract a line item by ID from the model.
        
        Note that the first line item with the given id will be returned.
        """
        for case in self.cases:
            for module in case.modules:
                for line_item in module.line_items:
                    if line_item.uid == line_item_id:
                        return line_item
                for cm in module.child_modules:
                    for cline_item in cm.line_items:
                        if cline_item.uid == line_item_id:
                            return cline_item
        raise Exception(f'cannot find line item with id {line_item_id}')

    def pull_case_by_id(self, id) -> Case:
        for case in self.cases:
            if case.uid == id:
                return case
        raise Exception('cannot find case with id')

    @property
    def first_case(self):
        return self.cases[0]

    @property
    def first_case_id(self):
        return self.first_case.uid

    @classmethod
    def from_json(cls, data):
        return cls(uid=data[cls.fields.ID],
                   cases=list(
                       map(Case.from_json,
                           data[cls.fields.EDGES][cls.fields.CASES])))


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
