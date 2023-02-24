from dataclasses import dataclass

import pytest

from valsys.modeling.model.model import Model, ModelInformation
from valsys.modeling.model.tests.factories import model_factory


class TestModelInformation:

    @property
    def valid_uid(self):
        return 'uid42'

    @property
    def valid_tags(self):
        return ['t1', 't2']

    def test_init(self):
        uid = self.valid_uid
        mi = ModelInformation(uid=uid)
        assert mi.uid == uid
        assert len(mi.tags) == 0
        assert len(mi.cases) == 0
        assert mi.data_sources == ''

    def test_from_json_tags_only(self):
        uid = self.valid_uid
        tags = self.valid_tags
        ij = {ModelInformation.fields.TAGS: tags}
        mi = ModelInformation.from_json(uid=uid, input_json=ij)
        assert mi.tags == tags
        assert len(mi.cases) == 0
        assert mi.data_sources == ''

    def test_from_json_tags_only_empty(self):
        uid = self.valid_uid
        ij = {ModelInformation.fields.TAGS: []}
        mi = ModelInformation.from_json(uid=uid, input_json=ij)
        assert mi.tags == []

    def test_from_json_data_source_only(self):
        uid = self.valid_uid
        data_source = 'data'
        ij = {ModelInformation.fields.DATA_SOURCES: data_source}
        mi = ModelInformation.from_json(uid=uid, input_json=ij)
        assert mi.data_sources == data_source




@dataclass
class FakeCase:
    case: str


class TestModel:

    def model_base(self, uid=None) -> Model:
        return Model(uid=uid or self.valid_uid)

    def model_n_cases(self, uid, n) -> Model:
        model = self.model_base(uid=uid)
        for c in range(n):
            model.cases.append(FakeCase(str(c)))
        return model

    @property
    def valid_uid(self):
        return 'uid42'

    def test_init(self):
        uid = self.valid_uid
        m = self.model_base(uid=uid)
        assert len(m.cases) == 0
        assert m.uid == uid

    def test_model_with_cases(self):
        uid = self.valid_uid
        model = self.model_n_cases(uid, 4)
        assert len(model.cases) == 4

    def test_pull_module_found(self):
        model = model_factory()
        m = model.pull_module('0')
        assert m.uid == '0'
        assert m.name == 'module 0'

    def test_pull_module_found_2(self):
        model = model_factory(nmodules=5)
        m = model.pull_module('3')
        assert m.uid == '3'
        assert m.name == 'module 3'

    def test_pull_child_module_found(self):
        model = model_factory()
        m = model.pull_module('00')
        assert m.uid == '00'
        assert m.name == 'module 0 child 0'

    def test_pull_child_module_found_2(self):
        model = model_factory(nchild_modules=5)
        m = model.pull_module('03')
        assert m.uid == '03'
        assert m.name == 'module 0 child 3'

    def test_pull_child_module_found_22(self):
        model = model_factory(nmodules=3, nchild_modules=5)
        m = model.pull_module('23')
        assert m.uid == '23'
        assert m.name == 'module 2 child 3'

    def test_pull_module_not_found(self):
        model = model_factory()
        with pytest.raises(Exception) as err:
            model.pull_module('garbage')
        assert 'cannot find module with id' in str(err)

    def test_pull_module_by_name_found(self):
        model = model_factory()
        m = model.pull_module_by_name('module 0')
        assert m.uid == '0'

    def test_pull_module_by_name_child_found(self):
        model = model_factory()
        m = model.pull_module_by_name('module 0 child 0')
        assert m.uid == '00'

    def test_pull_module_by_name_not_found(self):
        model = model_factory()
        with pytest.raises(Exception) as err:
            model.pull_module_by_name('garbage')
        assert 'cannot find module with name' in str(err)

    def test_pull_line_item_not_found(self):
        model = model_factory()
        with pytest.raises(Exception) as err:
            model.pull_line_item('garbage')
        assert 'cannot find line item with id' in str(err)

    def test_pull_line_item_found(self):
        model = model_factory()
        lin = model.pull_line_item('0l0')
        assert lin.name == 'module 0 li 0'

    def test_pull_case_by_id_found(self):
        model = model_factory()
        case = model.pull_case_by_id('1')
        assert case.uid == '1'

    def test_pull_case_by_id_not_found(self):
        model = model_factory()
        with pytest.raises(Exception) as err:
            model.pull_case_by_id('garbage')
        assert 'cannot find case with id' in str(err)

    def test_first_case(self):
        model = model_factory()
        fc = model.first_case
        assert fc.uid == '1'

    def test_first_case_id(self):
        model = model_factory()
        assert model.first_case_id == '1'
