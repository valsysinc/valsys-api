from valsys.modeling.model.model import ModelInformation, Model
from valsys.modeling.model.case import Case
from valsys.modeling.model.module import Module
import pytest


class TestModelInformation:

    @property
    def valid_uid(self):
        return 'uid42'

    def test_init(self):
        uid = self.valid_uid
        mi = ModelInformation(uid=uid)
        assert mi.uid == uid
        assert len(mi.tags) == 0
        assert len(mi.cases) == 0
        assert mi.data_sources == ''

    def test_from_json_tags_only(self):
        uid = self.valid_uid
        ij = {ModelInformation.fields.TAGS: 't1,t2'}
        mi = ModelInformation.from_json(uid=uid, input_json=ij)
        assert mi.tags == ['t1', 't2']
        assert len(mi.cases) == 0
        assert mi.data_sources == ''

    def test_from_json_tags_only_empty(self):
        uid = self.valid_uid
        ij = {ModelInformation.fields.TAGS: ''}
        mi = ModelInformation.from_json(uid=uid, input_json=ij)
        assert mi.tags == []

    def test_from_json_data_source_only(self):
        uid = self.valid_uid
        data_source = 'data'
        ij = {ModelInformation.fields.DATA_SOURCES: data_source}
        mi = ModelInformation.from_json(uid=uid, input_json=ij)
        assert mi.data_sources == data_source


from dataclasses import dataclass


@dataclass
class FakeCase:
    case: str


def model_factory(model_id='uid42', nmodules=2, nchild_modules=1):

    cid = '1'
    start_period = 2019

    modules = []
    for m in range(nmodules):
        parent_module_name = f"module {m}"
        parent_module_id = str(m)
        child_module_names = []
        for cmn in range(nchild_modules):
            child_module_names.append((f"{parent_module_id}{cmn}",
                                       f"{parent_module_name} child {cmn}"))

        modules.append({
            Module.fields.ID: parent_module_id,
            Module.fields.NAME: parent_module_name,
            Module.fields.MODULE_START: start_period,
            Module.fields.EDGES: {
                Module.fields.CHILD_MODULES: [{
                    Module.fields.ID:
                    cid,
                    Module.fields.NAME:
                    cmn,
                    Module.fields.MODULE_START:
                    start_period
                } for cid, cmn in child_module_names]
            }
        })

    return Model.from_json({
        Model.fields.ID: model_id,
        Model.fields.EDGES: {
            Model.fields.CASES: [{
                Case.fields.ID: cid,
                Case.fields.START_PERIOD: start_period,
                Case.fields.EDGES: {
                    Case.fields.MODULES: modules
                }
            }]
        }
    })


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