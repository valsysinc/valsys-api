from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.model.module import Module


def module_with_no_children():
    mj = {
        Module.fields.ID: '1234',
        Module.fields.NAME: 'module name',
        Module.fields.MODULE_START: 2018,
        Module.fields.EDGES: {
            Module.fields.LINE_ITEMS: [{
                LineItem.fields.ID: 42,
                LineItem.fields.NAME: 'Name',
                LineItem.fields.EDGES: {
                    LineItem.fields.FACTS: [{
                        Fact.fields.UID: '1234',
                        Fact.fields.PERIOD: 2019
                    }, {
                        Fact.fields.UID: '12345',
                        Fact.fields.PERIOD: 2019
                    }, {
                        Fact.fields.UID: '12345',
                        Fact.fields.PERIOD: 2020
                    }]
                }
            }]
        }
    }
    return Module.from_json(mj)


def module_with_line_items_with_tags():
    mj = {
        Module.fields.ID: '1234',
        Module.fields.NAME: 'module name',
        Module.fields.MODULE_START: 2018,
        Module.fields.EDGES: {
            Module.fields.LINE_ITEMS: [{
                LineItem.fields.ID: 42,
                LineItem.fields.NAME: 'Name',
                LineItem.fields.TAGS: ['t1', 't2']
            }, {
                LineItem.fields.ID: 422,
                LineItem.fields.NAME: 'Name2',
            }, {
                LineItem.fields.ID: 43,
                LineItem.fields.NAME: 'Name3',
                LineItem.fields.TAGS: ['t1', 't3']
            }],
            Module.fields.CHILD_MODULES: [{
                Module.fields.ID: 91,
                Module.fields.NAME: 'child1',
                Module.fields.MODULE_START: 2019,
                Module.fields.EDGES: {
                    Module.fields.LINE_ITEMS: [{
                        LineItem.fields.ID:
                        421,
                        LineItem.fields.NAME:
                        'Name1',
                        LineItem.fields.TAGS: ['t11', 't12']
                    }, {
                        LineItem.fields.ID:
                        431,
                        LineItem.fields.NAME:
                        'Name2',
                        LineItem.fields.TAGS: ['t11', 't13']
                    }]
                },
            }]
        },
    }
    return Module.from_json(mj)


def module_with_n_children():
    mj = {
        Module.fields.ID: '1234',
        Module.fields.NAME: 'module name',
        Module.fields.MODULE_START: 2018,
        Module.fields.EDGES: {
            Module.fields.LINE_ITEMS: [{
                LineItem.fields.ID: 42,
                LineItem.fields.NAME: 'Name'
            }],
            Module.fields.CHILD_MODULES: [{
                Module.fields.ID: 91,
                Module.fields.NAME: 'child1',
                Module.fields.MODULE_START: 2019,
                Module.fields.EDGES: {
                    Module.fields.CHILD_MODULES: [{
                        Module.fields.ID:
                        91,
                        Module.fields.NAME:
                        'child2',
                        Module.fields.MODULE_START:
                        2019
                    }]
                }
            }]
        }
    }
    return Module.from_json(mj)


class TestModule:

    def test_init(self):
        uid = '1234'
        name = 'Name'
        module_start = 2019
        module = Module(uid=uid, name=name, module_start=module_start)
        assert module.uid == uid
        assert module.name == name
        assert module.module_start == module_start
        assert len(module.line_items) == 0
        assert len(module.child_modules) == 0

        mm = module.module_meta
        assert mm.get(Module.fields.NAME) == name
        assert mm.get(Module.fields.ID) == uid
        assert mm.get('children') == []

    def test_from_json(self):

        mj = {
            Module.fields.ID: '1234',
            Module.fields.NAME: 'module name',
            Module.fields.MODULE_START: 2018,
            Module.fields.EDGES: {
                Module.fields.LINE_ITEMS: [{
                    Module.fields.ID: 42,
                    'name': 'Name'
                }],
                Module.fields.CHILD_MODULES: [{
                    Module.fields.ID: 91,
                    Module.fields.NAME: 'child1',
                    Module.fields.MODULE_START: 2019
                }]
            }
        }
        module = Module.from_json(mj)
        assert module.uid == mj.get(Module.fields.ID)
        assert module.name == mj.get('name')
        assert module.module_start == mj.get(Module.fields.MODULE_START)
        assert len(module.line_items) == 1
        assert len(module.child_modules) == 1

    def test_from_json_no_child_modules(self):

        mj = {
            Module.fields.ID: '1234',
            Module.fields.NAME: 'module name',
            Module.fields.MODULE_START: 2018,
            'edges': {
                Module.fields.LINE_ITEMS: [{
                    LineItem.fields.ID: 42,
                    'name': 'Name'
                }]
            }
        }
        module = Module.from_json(mj)
        assert module.uid == mj.get(Module.fields.ID)
        assert module.name == mj.get('name')
        assert module.module_start == mj.get(Module.fields.MODULE_START)
        assert len(module.line_items) == 1
        assert len(module.child_modules) == 0

    def test_find_module_not_found(self):

        module = module_with_no_children()
        assert module.find_module('someModule') is None

    def test_find_module_no_depth(self):
        module = module_with_n_children()
        fm = module.find_module('child1')
        assert fm.name == 'child1'

    def test_find_module_depth(self):
        module = module_with_n_children()
        fm = module.find_module('child2')
        assert fm.name == 'child2'

    def test_find_module_depth_not_found(self):
        module = module_with_n_children()
        fm = module.find_module('child3')
        assert fm is None

    def test_pull_line_items_from_tags(self):
        module = module_with_line_items_with_tags()
        items = module.pull_items_from_tags(['t1'])
        assert len(items) == 2

    def test_pull_line_items_from_tags_within_children(self):
        module = module_with_line_items_with_tags()
        items = module.pull_items_from_tags(['t11'])
        assert len(items) == 2

    def test_pull_line_items_from_tags_within_children_and_root(self):
        module = module_with_line_items_with_tags()
        items = module.pull_items_from_tags(['t1', 't11'])
        assert len(items) == 4

    def test_pull_line_item_by_name_found(self):
        tgt_name = 'Name'
        module = module_with_line_items_with_tags()
        item = module.pull_item_by_name(tgt_name)
        assert item.name == tgt_name

    def test_pull_line_item_by_name_not_found(self):
        tgt_name = 'garbage'
        module = module_with_line_items_with_tags()
        item = module.pull_item_by_name(tgt_name)
        assert item is None

    def test_periods(self):
        module = module_with_no_children()
        assert module.periods == [2019, 2020]
