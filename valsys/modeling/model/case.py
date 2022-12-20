from dataclasses import dataclass, field
from typing import List

from .line_item import LineItem
from .module import Module


@dataclass
class CaseInformation:
    uid: str
    case: str

    @classmethod
    def from_json(cls, input_json):
        return cls(uid=input_json.get("uid"), case=input_json.get("case"))


@dataclass
class Case:
    uid: str
    start_period: float
    case: str
    modules: List[Module] = field(default_factory=list)
    ticker: str = ""

    @property
    def module_meta(self):
        return [module.module_meta for module in self.modules]

    def set_ticker(self, ticker):
        self.ticker = ticker

    def pull_module(self, name: str) -> Module:
        if self.modules is None:
            return None
        for module in self.modules:
            if module.name == name:
                return module
            target = module.find_module(name)
            if target is not None:
                return target
        raise ValueError(f"cannot find module with name {name}")
        # return None

    def pull_items_from_tags(self, tags: List[str]) -> List[LineItem]:
        items = []
        for module in self.modules:
            target_items = module.pull_items_from_tags(tags)
            if target_items is not None:
                items += target_items
        return items

    @classmethod
    def from_json(cls, data):

        return cls(
            uid=data["id"],
            start_period=data["startPeriod"],
            #case=data["case"],
            case="",
            modules=list(map(Module.from_json, data['edges']["modules"])),
        )
