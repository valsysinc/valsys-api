from valsys.modeling.model.case import Case
import pytest
import uuid


def case_factory(uid='1234', start_period=2019, case_name='Case name') -> Case:

    return Case(uid=uid, start_period=start_period, case=case_name)


from typing import List
from dataclasses import dataclass, field


@dataclass
class FakeModule:
    id: str
    name: str
    child_modules: List['FakeModule'] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def find_module(self, name):
        for m in self.child_modules:
            if m.name == name:
                return m

    def pull_items_from_tags(self, tags):
        return self.tags

    @property
    def uid(self):
        return self.id


def fake_uuid():
    return str(uuid.uuid1())


class TestCase:

    def test_init(self):
        uid = '1234'
        start_period = 2019
        case_name = 'Case name'
        ticker = 'TKR'
        case = case_factory(uid=uid,
                            start_period=start_period,
                            case_name=case_name)
        assert case.uid == uid
        assert case.start_period == start_period
        assert case.case == case_name
        assert case.ticker == ''
        case.set_ticker(ticker)
        assert case.ticker == ticker

    def test_first_module_err(self):
        uid = '1234'
        start_period = 2019
        case_name = 'Case name'
        case = case_factory(uid=uid,
                            start_period=start_period,
                            case_name=case_name)
        with pytest.raises(Exception) as err:
            case.first_module
        assert 'no modules in case' in str(err)

    def test_first_module_ok(self):
        case = case_factory()
        case.modules.append(42)
        assert case.first_module == 42
        case.modules.append(43)
        assert case.first_module == 42
        case.modules.append(44)
        assert case.first_module == 42

    def test_pull_module_no_modules(self):
        case = case_factory()
        with pytest.raises(ValueError) as err:
            case.pull_module('modulename')
        assert 'cannot find module with name' in str(err)

    def test_pull_module_one_module(self):
        case = case_factory()
        m = FakeModule(name='modulename', id=fake_uuid())
        case.modules = [m]
        assert case.pull_module('modulename') == m

    def test_pull_module_multiple_module(self):
        case = case_factory()
        m1 = FakeModule(name='modulename1', id=fake_uuid())
        m2 = FakeModule(name='modulename2', id=fake_uuid())
        case.modules = [m1, m2]
        assert case.pull_module('modulename1') == m1
        assert case.pull_module('modulename2') == m2

    def test_pull_module_child_module(self):
        case = case_factory()
        m2 = FakeModule(name='modulename2', id=fake_uuid())
        m1 = FakeModule(name='modulename1', id=fake_uuid(), child_modules=[m2])
        case.modules = [m1]
        assert case.pull_module('modulename2') == m2

    def test_pull_module_by_id_ok(self):
        case = case_factory()
        m1 = FakeModule(name='modulename1', id=fake_uuid())
        m2 = FakeModule(name='modulename2', id=fake_uuid())
        case.modules = [m1, m2]
        assert case.pull_module_by_id(m1.id) == m1
        assert case.pull_module_by_id(m2.id) == m2

    def test_pull_module_by_id_child(self):
        case = case_factory()
        m2 = FakeModule(name='modulename2', id=fake_uuid())
        m1 = FakeModule(name='modulename1', id=fake_uuid(), child_modules=[m2])
        case.modules = [m1]
        assert case.pull_module_by_id(m1.id) == m1
        assert case.pull_module_by_id(m2.id) == m2

    def test_pull_items_from_tags_no_modules(self):
        case = case_factory()
        assert case.pull_items_from_tags(None) == []

    def test_pull_items_from_tags_found(self):
        case = case_factory()
        m1 = FakeModule(name='modulename1', id=fake_uuid())
        m1.tags = ['11', '12']
        m2 = FakeModule(name='modulename2', id=fake_uuid())
        m2.tags = ['21', '22']
        case.modules = [m1, m2]
        assert case.pull_items_from_tags('None') == ['11', '12', '21', '22']
