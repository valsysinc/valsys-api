from valsys.modeling.model.module import Module


def module_with_no_children():
    mj = {
        'uid': '1234',
        'name': 'module name',
        'moduleStart': 2018,
        'lineItems': [{
            'uid': 42,
            'name': 'Name'
        }]
    }
    return Module.from_json(mj)


def module_with_line_items_with_tags():
    mj = {
        'uid':
        '1234',
        'name':
        'module name',
        'moduleStart':
        2018,
        'lineItems': [{
            'uid': 42,
            'name': 'Name',
            'tags': ['t1', 't2']
        }, {
            'uid': 422,
            'name': 'Name2',
        }, {
            'uid': 43,
            'name': 'Name3',
            'tags': ['t1', 't3']
        }],
        'childModules': [{
            'uid':
            91,
            'name':
            'child1',
            'moduleStart':
            2019,
            'lineItems': [{
                'uid': 421,
                'name': 'Name1',
                'tags': ['t11', 't12']
            }, {
                'uid': 431,
                'name': 'Name2',
                'tags': ['t11', 't13']
            }],
        }]
    }
    return Module.from_json(mj)


def module_with_n_children():
    mj = {
        'uid':
        '1234',
        'name':
        'module name',
        'moduleStart':
        2018,
        'lineItems': [{
            'uid': 42,
            'name': 'Name'
        }],
        'childModules': [{
            'uid':
            91,
            'name':
            'child1',
            'moduleStart':
            2019,
            'childModules': [{
                'uid': 91,
                'name': 'child2',
                'moduleStart': 2019
            }]
        }]
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
        assert mm.get('name') == name
        assert mm.get('uid') == uid
        assert mm.get('children') == []

    def test_from_json(self):

        mj = {
            'uid': '1234',
            'name': 'module name',
            'moduleStart': 2018,
            'lineItems': [{
                'uid': 42,
                'name': 'Name'
            }],
            'childModules': [{
                'uid': 91,
                'name': 'child1',
                'moduleStart': 2019
            }]
        }
        module = Module.from_json(mj)
        assert module.uid == mj.get('uid')
        assert module.name == mj.get('name')
        assert module.module_start == mj.get('moduleStart')
        assert len(module.line_items) == 1
        assert len(module.child_modules) == 1

    def test_from_json_no_child_modules(self):

        mj = {
            'uid': '1234',
            'name': 'module name',
            'moduleStart': 2018,
            'lineItems': [{
                'uid': 42,
                'name': 'Name'
            }]
        }
        module = Module.from_json(mj)
        assert module.uid == mj.get('uid')
        assert module.name == mj.get('name')
        assert module.module_start == mj.get('moduleStart')
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
