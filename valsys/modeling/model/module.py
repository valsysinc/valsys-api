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

    class fields:
        ID = 'id'
        NAME = 'name'
        LINE_ITEMS = 'lineItems'
        CHILD_MODULES = 'childModules'
        MODULE_START = 'moduleStart'
        EDGES = 'edges'

    @property
    def module_meta(self):
        return {
            self.fields.NAME: self.name,
            self.fields.ID: self.uid,
            'children': [m.module_meta for m in self.child_modules or []]
        }

    def find_module(self, name: str) -> "Module":
        """Returns a child module by name.
        
        If no matching module is found, `None` is returned.
        """
        for child_module in self.child_modules:
            if child_module.name == name:
                return child_module
            target = child_module.find_module(name)
            if target is not None:
                return target
        return None

    @property
    def last_line_item(self):
        l = len(self.line_items)
        return self.line_items[l - 1]

    def pull_items_from_tags(self, tags: List[str]) -> List[LineItem]:
        items = []

        for item in self.line_items:
            for tag in tags:
                if tag in item.tags:
                    items.append(item)

        for child_module in self.child_modules:
            tagged_items = child_module.pull_items_from_tags(tags)
            if tagged_items != None:
                items += tagged_items
        for item in items:
            sorted_facts = sorted(item.facts, key=lambda f: f.period)
            item.facts = sorted_facts
        return items

    @property
    def periods(self) -> List[float]:
        periods = set()
        for fact in self.line_items[0].facts:
            periods.add(fact.period)
        pl = list(periods)
        pl.sort()
        return pl

    def pull_item_by_name(self, name: str) -> LineItem:
        """Extract and return the line item with
        the provided name.
        
        If none is found, `None` is returned."""
        #TODO: PFL-24
        # should this look at the line items of the modules' children modules too?
        if self.line_items is not None:
            for item in self.line_items:
                if item.name == name:
                    return item
        return None

    @classmethod
    def from_json(cls, data):
        return cls(
            uid=data[cls.fields.ID],
            name=data[cls.fields.NAME],
            module_start=data[cls.fields.MODULE_START],
            line_items=list(
                map(
                    LineItem.from_json,
                    data.get(cls.fields.EDGES, {}).get(cls.fields.LINE_ITEMS,
                                                       []))),
            child_modules=list(
                map(
                    Module.from_json,
                    data.get(cls.fields.EDGES,
                             {}).get(cls.fields.CHILD_MODULES, []))),
        )
