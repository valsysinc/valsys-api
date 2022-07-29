from valsys.modeling.model.model import ModelInformation


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
