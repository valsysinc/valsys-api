from dataclasses import dataclass
from unittest import mock

import pytest

from valsys.modeling.exceptions import FilterModelsException
from valsys.modeling.models import (
    ModelDetailInformationWithFields,
    ModelGroup,
    ModelsFilter,
    PermissionTypes,
    Permissions,
)

from .factories import valid_models_filter


MODULE_PREFIX = 'valsys.modeling.models'


class TestPermissions:

    @pytest.mark.parametrize("permission", PermissionTypes.types())
    def test_works_ok(self, permission):
        p = Permissions(permission)
        assert p.jsonify() == {permission: True}


class TestModelGroup:

    def test_works_ok(self):
        uid, name, user_id, model_ids = 'u', 'n', 'ui', ['1', '2']
        mg = ModelGroup(uid=uid,
                        name=name,
                        user_id=user_id,
                        model_ids=model_ids)
        assert mg.uid == uid
        assert mg.name == name
        assert mg.user_id == user_id
        assert mg.model_ids == model_ids

    def test_jsonify(self):
        uid, name, user_id, model_ids = 'u', 'n', 'ui', ['1', '2']
        mg = ModelGroup(uid=uid,
                        name=name,
                        user_id=user_id,
                        model_ids=model_ids)
        j = mg.jsonify()
        assert j.get('uid') == uid
        assert j.get('name') == name
        assert j.get('userID') == user_id
        assert j.get('modelIDs') == model_ids

    def test_from_json(self):
        uid, name, user_id, model_ids = 'u', 'n', 'ui', ['1', '2']
        jd = {
            'uid': uid,
            'name': name,
            'userID': user_id,
            'modelIDs': model_ids
        }
        mg_from_j = ModelGroup.from_json(jd)
        assert mg_from_j.uid == uid
        assert mg_from_j.name == name
        assert mg_from_j.user_id == user_id
        assert mg_from_j.model_ids == model_ids


class TestModelsFilter:

    @property
    def valid_max_date(self):
        return '1234'

    @property
    def valid_min_date(self):
        return '5678'

    def test_init(self):
        max_date = self.valid_max_date
        min_date = self.valid_min_date
        predicate = 'hello'
        model_type = ModelsFilter.ValidTypes.MODEL_TYPES[0]
        mf = ModelsFilter(max_date=max_date,
                          min_date=min_date,
                          predicate=predicate,
                          model_type=model_type)

        assert mf.max_date == max_date
        assert mf.min_date == min_date
        assert mf.predicate == predicate
        assert mf.model_type == model_type
        assert not mf.filter_geography
        assert not mf.filter_industry
        assert not mf.filter_name
        assert not mf.filter_ticker

    def test_set_filter_on_blank(self):
        mf = valid_models_filter()
        mf.set_filter_on(None)
        assert not mf.filter_name
        assert not mf.filter_geography
        assert not mf.filter_industry
        assert not mf.filter_ticker

    def test_set_filter_on_name_only(self):
        mf = valid_models_filter()
        mf.set_filter_on(['naMe'])
        assert mf.filter_name
        assert not mf.filter_geography
        assert not mf.filter_industry
        assert not mf.filter_ticker

    def test_set_filter_on_name_ticker_geog_industry(self):
        mf = valid_models_filter()
        mf.set_filter_on(['naMe', 'indusTry', 'Geography', 'TickeR'])
        assert mf.filter_name
        assert mf.filter_geography
        assert mf.filter_industry
        assert mf.filter_ticker

    def test_invalid_filter_type(self):
        max_date = self.valid_max_date
        min_date = self.valid_min_date
        predicate = 'hello'
        tag_filter_type = 'garbage'
        model_type = ModelsFilter.ValidTypes.MODEL_TYPES[0]
        with pytest.raises(FilterModelsException) as err:
            ModelsFilter(max_date=max_date,
                         min_date=min_date,
                         predicate=predicate,
                         model_type=model_type,
                         tag_filter_type=tag_filter_type)
        assert tag_filter_type in str(err)

    def test_invalid_model_type(self):
        max_date = self.valid_max_date
        min_date = self.valid_min_date
        predicate = 'hello'
        model_type = 'garbage'
        with pytest.raises(FilterModelsException) as err:
            ModelsFilter(max_date=max_date,
                         min_date=min_date,
                         predicate=predicate,
                         model_type=model_type)
        assert model_type in str(err)

    def test_jsonify_with_name_geography_filters(self):
        max_date = self.valid_max_date
        min_date = self.valid_min_date
        predicate = 'hello'
        model_type = ModelsFilter.ValidTypes.MODEL_TYPES[0]
        mf = ModelsFilter(max_date=max_date,
                          min_date=min_date,
                          predicate=predicate,
                          model_type=model_type)
        mf.set_filter_on(['naMe', 'Geography'])

        mf_j = mf.jsonify()
        assert mf_j.get('maxDate') == max_date
        assert mf_j.get('minDate') == min_date
        assert not mf_j.get('filters').get('Ticker')
        assert mf_j.get('filters').get('Geography')
        assert not mf_j.get('filters').get('Industry')
        assert mf_j.get('filters').get('Name')


@dataclass
class ModelDetailInformation:
    uid: str
    ticker: str

    @classmethod
    def from_json(cls, j):
        return cls(uid=j.get('uid'), ticker=j.get('ticker'))


class TestModelDetailInformationWithFields:

    def test_init(self):
        mdiwf = ModelDetailInformationWithFields(
            model=ModelDetailInformation(uid='1234', ticker='TKR'))
        assert mdiwf.fields == {}
        assert mdiwf.uid == '1234'
        assert mdiwf.ticker == 'TKR'

    @mock.patch(f"{MODULE_PREFIX}.ModelDetailInformation")
    def test_from_json_with_model(self, mock_ModelDetailInformation):
        flds = {'f': 1}
        j = {'model': 42, 'fields': flds}
        mdiwf = ModelDetailInformationWithFields.from_json(j)
        mock_ModelDetailInformation.from_json.assert_called_once_with(42)
        assert mdiwf.fields == flds

    @mock.patch(f"{MODULE_PREFIX}.ModelDetailInformation")
    def test_from_json_without_model(self, mock_ModelDetailInformation):

        j = {'info': 42}
        mdiwf = ModelDetailInformationWithFields.from_json(j)
        mock_ModelDetailInformation.from_json.assert_called_once_with(j)
        assert mdiwf.fields == {}
