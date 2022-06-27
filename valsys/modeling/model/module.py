from typing import List
from dataclasses import dataclass, field

# from valsys.modeling.service import add_item
from .line_item import LineItem


@dataclass
class Module:
    uid: str
    name: str
    module_start: int
    line_items: List[LineItem] = field(default_factory=list)
    child_modules: List["Module"] = field(default_factory=list)

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

    # def add_item(self, name, order, modelID, caseID):
    #    module_json = add_item(caseID, modelID, name, order, self.uid)
    #    module = Module.from_json(module_json["module"])
    #    for l in module.line_items:
    #        if l.name == name:
    #            return l

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

    # def add_child_module(self, name, modelID, caseID):
    #    return Module.from_json(add_child_module(self.uid, name, modelID, caseID))

    @classmethod
    def from_json(cls, data):
        line_items = []
        if data.get("lineItems"):
            line_items = list(map(LineItem.from_json, data["lineItems"]))
        if data.get("childModules") is not None:
            child_modules = list(map(Module.from_json, data["childModules"]))
            return cls(
                data["uid"],
                data["name"],
                data["moduleStart"],
                line_items,
                child_modules,
            )
        return cls(data["uid"], data["name"], data["moduleStart"], line_items, None)
