from dataclasses import dataclass, field
from typing import List

from .line_item import LineItem


@dataclass
class Module:
    uid: str
    name: str
    module_start: int
    line_items: List[LineItem] = field(default_factory=list)
    child_modules: List["Module"] = field(default_factory=list)

    @property
    def module_meta(self):
        return {
            'name': self.name,
            'uid': self.uid,
            'children': [m.module_meta for m in self.child_modules or []]
        }

    def find_module(self, name: str) -> "Module":
        if self.child_modules is None:
            return None
        for child_module in self.child_modules:
            if child_module.name == name:
                return child_module
            target = child_module.find_module(name)
            if target is not None:
                return target
        return None

    def pull_items_from_tags(self, tags: List[str]) -> List[LineItem]:
        items = []
        if self.line_items is not None:
            for item in self.line_items:
                if item.tags is not None:
                    for tag in tags:
                        if tag in item.tags:
                            items.append(item)
        if self.child_modules is not None:
            for child_module in self.child_modules:
                tagged_items = child_module.pull_items_from_tags(tags)
                if tagged_items != None:
                    items += tagged_items
        for item in items:
            sorted_facts = sorted(item.facts, key=lambda f: f.period)
            item.facts = sorted_facts
        return items

    def pull_item_by_name(self, name: str) -> LineItem:

        if self.line_items is not None:
            for item in self.line_items:
                if item.name == name:
                    return item
        return None

    @classmethod
    def from_json(cls, data):
        if data.get("childModules") is not None:
            child_modules = list(map(Module.from_json, data["childModules"]))
        else:
            child_modules = None
        return cls(
            uid=data["uid"],
            name=data["name"],
            module_start=data["moduleStart"],
            line_items=list(map(LineItem.from_json, data.get("lineItems",
                                                             []))),
            child_modules=child_modules,
        )
