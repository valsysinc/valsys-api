from .module import Module
from typing import List
from .line_item import LineItem
from dataclasses import dataclass, field


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
            uid=data["uid"],
            start_period=data["startPeriod"],
            case=data["case"],
            modules=list(map(Module.from_json, data["modules"])),
        )
