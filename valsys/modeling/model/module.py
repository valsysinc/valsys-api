from dataclasses import dataclass, field
from typing import List

from .line_item import LineItem


@dataclass
class Module:
    uid: str
    name: str
    module_start: int
    module_end: int = 0
    depth: int = 0
    order: int = 1
    period_type: str = 'ANNUAL'
    start_period: float = 2019
    unlinked: bool = False
    line_items: List[LineItem] = field(default_factory=list)
    child_modules: List["Module"] = field(default_factory=list)

    class fields:
        UID = 'id'
        DEPTH = 'depth'
        ORDER = 'order'
        NAME = 'name'
        MODULE_START = 'moduleStart'
        MODULE_END = 'moduleEnd'
        LINE_ITEMS = 'lineItems'
        PERIOD_TYPE = 'periodType'
        START_PERIOD = "startPeriod"
        CHILD_MODULES = 'childModules'
        UNLINKED = 'unlinked'
        EDGES = 'edges'

    @property
    def module_meta(self):
        return {
            'name': self.name,
            'uid': self.uid,
            'children': [m.module_meta for m in self.child_modules or []]
        }

    def find_module(self, name: str) -> "Module":
        """Returns a module by name.
        
        If no matching module is found, `None` is returned.
        """
        for child_module in self.child_modules:
            if child_module.name == name:
                return child_module
            target = child_module.find_module(name)
            if target is not None:
                return target
        return None

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

    def pull_item_by_name(self, name: str) -> LineItem:
        """Extract and return the line item with
        the provided name.
        
        If none is found, `None` is returned."""
        if self.line_items is not None:
            for item in self.line_items:
                if item.name == name:
                    return item
        return None

    @classmethod
    def from_json(cls, data):
        return cls(
            uid=data[cls.fields.UID],
            depth=data.get(cls.fields.DEPTH, 0),
            name=data[cls.fields.NAME],
            module_start=data[cls.fields.MODULE_START],
            module_end=data.get(cls.fields.MODULE_END, 0),
            order=data.get(cls.fields.ORDER),
            period_type=data.get(cls.fields.PERIOD_TYPE),
            start_period=data.get(cls.fields.START_PERIOD),
            unlinked=data.get(cls.fields.UNLINKED, False),
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

    def jsonify(self):
        return {
            self.fields.UID: self.uid,
            self.fields.DEPTH: self.depth,
            self.fields.NAME: self.name,
            self.fields.MODULE_START: self.module_start,
            self.fields.MODULE_END: self.module_end,
            self.fields.ORDER: self.order,
            self.fields.PERIOD_TYPE: self.period_type,
            self.fields.START_PERIOD: self.start_period,
            self.fields.UNLINKED: self.unlinked,
            self.fields.EDGES: {
                self.fields.LINE_ITEMS: [l.jsonify() for l in self.line_items],
                self.fields.CHILD_MODULES:
                [cm.jsonify() for cm in self.child_modules]
            }
        }