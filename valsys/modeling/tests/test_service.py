from dataclasses import dataclass
from unittest import mock

import pytest

from valsys.modeling.client.exceptions import (
    ModelingServiceGetException,
    ModelingServicePostException,
)
from valsys.modeling.exceptions import (
    AddChildModuleException,
    AddLineItemException,
    NewModelGroupsException,
    PullModelGroupsException,
    PullModelInformationException,
    RecalculateModelException,
    RemoveModuleException,
    ShareModelException,
    TagLineItemException,
    TagModelException,
    UpdateModelGroupsException,
)
from valsys.modeling.vars import Headers

from valsys.modeling.model.line_item import LineItem
import valsys.modeling.service as Modeling
from valsys.modeling.service import (SpawnedModelInfo)
from valsys.modeling.vars import Vars
from valsys.spawn.exceptions import ModelSpawnException
from valsys.modeling.models import ModelGroups, ModelGroup
from .factories import (
    valid_email,
    valid_name,
    valid_permission,
    valid_tags,
    valid_ticker,
    valid_uid,
    valid_uids,
)
from valsys.modeling.client.urls import VSURL

MODULE_PREFIX = "valsys.modeling.service"


class TestFilterUserModels:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.ModelDetailInformationWithFields.from_json")
    def test_works_ok_no_args(self,
                              mock_ModelDetailInformationWithFields_from_json,
                              mock_new_client):
        mock_client = mock.MagicMock()
        mock_client.post.return_value = {'data': {'models': [1, 2]}}
        mock_new_client.return_value = mock_client
        Modeling.filter_user_models()
        mock_new_client.assert_called_once()
        mock_client.post.assert_called_once()
        calls = [mock.call(1), mock.call(2)]
        mock_ModelDetailInformationWithFields_from_json.assert_has_calls(calls)


class TestSpawnModel:

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_works_ok(self, mock_new_socket_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        fake_model_id, fake_model_ticker = valid_uid(), valid_ticker()
        fake_post_ret = {
            'models': [{
                SpawnedModelInfo.fields.MODEL_ID: fake_model_id,
                'status': Vars.SUCCESS,
                SpawnedModelInfo.fields.TICKER: fake_model_ticker
            }]
        }
        mock_c.post.return_value = fake_post_ret
        mock_new_socket_client.return_value = mock_c

        assert Modeling.spawn_model(config) == [
            SpawnedModelInfo(model_id=fake_model_id, ticker=fake_model_ticker)
        ]
        assert config.action == Modeling.ModelingActions.SPAWN_MODELS

        config.jsonify.assert_called_once()
        mock_new_socket_client.assert_called_once()

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_works_ok_no_success(self, mock_new_socket_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        fake_model_id, fake_model_ticker = 'ghjkrhdg', valid_ticker()
        fake_post_ret = {
            'models': [{
                SpawnedModelInfo.fields.MODEL_ID: fake_model_id,
                'status': 'garbage',
                SpawnedModelInfo.fields.TICKER: fake_model_ticker
            }]
        }
        mock_c.post.return_value = fake_post_ret
        mock_new_socket_client.return_value = mock_c
        with pytest.raises(ModelSpawnException) as err:
            assert Modeling.spawn_model(config) == []
            assert config.action == Modeling.ModelingActions.SPAWN_MODELS

        config.jsonify.assert_called_once()
        mock_new_socket_client.assert_called_once()

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_fails_if_no_model_id(self, mock_new_socket_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        fake_model_id, fake_model_ticker = None, valid_ticker()
        fake_post_ret = {
            'models': [{
                SpawnedModelInfo.fields.MODEL_ID: fake_model_id,
                'status': Vars.SUCCESS,
                SpawnedModelInfo.fields.TICKER: fake_model_ticker
            }]
        }
        mock_c.post.return_value = fake_post_ret
        mock_new_socket_client.return_value = mock_c
        with pytest.raises(ModelSpawnException) as err:
            Modeling.spawn_model(config)
        assert "no modelID in response" in str(err)

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_raises(self, mock_new_socket_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        data, code, url = 42, 1, 'www'
        mock_c.post.side_effect = ModelingServiceGetException(data, code, url)
        mock_new_socket_client.return_value = mock_c
        with pytest.raises(ModelSpawnException) as err:
            Modeling.spawn_model(config)
        assert 'error building model' in str(err)
        assert str(data) in str(err)
        assert str(code) in str(err)
        assert url in str(err)


class TestPullModelInformation:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.ModelInformation.from_json")
    def test_works_ok_frm_json(self, mock_ModelInformation_from_json,
                               mock_new_client):
        uid = valid_uid()
        mock_get = mock.MagicMock()
        mock_cases = mock.MagicMock()
        mock_model_info = mock.MagicMock()
        mock_get.return_value = {
            'status': Vars.SUCCESS,
            'data': {
                'models': [{
                    'model': mock_cases
                }]
            }
        }
        mock_new_client.return_value.get = mock_get
        mock_ModelInformation_from_json.return_value = mock_model_info
        model_info = Modeling.pull_model_information(uid)
        mock_new_client.assert_called_once()
        mock_get.assert_called_once()
        _, kw = mock_get.call_args
        assert kw.get('headers') == {'modelIds': uid}
        mock_ModelInformation_from_json.assert_called_once_with(
            uid, mock_cases)
        assert model_info == mock_model_info

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises(self, mock_new_client):
        mock_c = mock.MagicMock()
        d, c, u = 42, 42, 'www'
        mock_c.get.side_effect = ModelingServiceGetException(d, c, u)
        mock_new_client.return_value = mock_c
        model_id = valid_uid(), valid_tags()
        with pytest.raises(PullModelInformationException) as err:
            Modeling.pull_model_information(model_id)
        assert 'could not pull model info for model' in str(err)


class TestTagModel:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok_without_auth_token(self, mock_new_client):

        mock_c = mock.MagicMock()
        mock_post_ret = mock.MagicMock()

        mock_c.post.return_value = mock_post_ret
        mock_new_client.return_value = mock_c
        model_id, tags = valid_uid(), valid_tags()
        assert Modeling.tag_model(model_id, tags) == mock_post_ret

        mock_new_client.assert_called_once_with(None)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok_with_auth_token(self, mock_new_client):

        mock_c = mock.MagicMock()
        mock_post_ret = mock.MagicMock()

        mock_c.post.return_value = mock_post_ret
        mock_new_client.return_value = mock_c
        model_id, tags, auth_token = valid_uid(), valid_tags(), 't0k3n'
        assert Modeling.tag_model(model_id, tags,
                                  auth_token=auth_token) == mock_post_ret

        mock_new_client.assert_called_once_with(auth_token)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises(self, mock_new_client):

        mock_c = mock.MagicMock()
        mock_post_ret = mock.MagicMock()
        d, c, u = 42, 42, 'www'
        mock_c.post.side_effect = ModelingServicePostException(d, c, u)
        mock_new_client.return_value = mock_c
        model_id, tags = valid_uid(), valid_tags()
        with pytest.raises(TagModelException) as err:
            Modeling.tag_model(model_id, tags)
        assert 'error tagging model' in str(err)


class TestPullCase:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.Case.from_json")
    def test_works_ok(self, mock_Case_from_json, mock_new_client):
        uid = valid_uid()
        mock_get = mock.MagicMock()
        mock_cases = mock.MagicMock()
        mock_model_info = mock.MagicMock()
        mock_get.return_value = {'data': {'case': mock_cases}}
        mock_new_client.return_value.get = mock_get
        mock_Case_from_json.return_value = mock_model_info
        model_info = Modeling.pull_case(uid)
        mock_new_client.assert_called_once()
        mock_get.assert_called_once()
        _, kw = mock_get.call_args
        assert kw.get('headers') == {'caseID': uid}
        mock_Case_from_json.assert_called_once_with(mock_cases)
        assert model_info == mock_model_info


@dataclass
class FakeLineItem:
    name: str = ''


class TestAddLineItem:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.Module.from_json")
    def test_works_ok(self, mock_from_json, mock_new_client):
        mock_client = mock.MagicMock()
        name = 'n'
        new_line_item_id = 'ox1'
        mock_post = {
            "data": {
                'module': {
                    'lineItems': [{
                        'name': name,
                        'id': new_line_item_id
                    }]
                }
            }
        }  #mock.MagicMock()
        mock_client.post.return_value = mock_post
        mock_new_client.return_value = mock_client
        mock_module = mock.MagicMock()
        case_id, model_id, module_id, order = 'c', 'm', 'mi', 'o'
        fake_line_item = LineItem(name=name, uid=new_line_item_id)
        mock_module.line_items = [fake_line_item]
        mock_from_json.return_value = mock_module

        li = Modeling.add_line_item(case_id, model_id, module_id, name, order)
        mock_new_client.assert_called_once()
        assert li == fake_line_item
        _, kww = mock_client.post.call_args
        assert 'url' in kww
        kw = kww['data']
        assert kw['caseID'] == case_id
        assert kw['modelID'] == model_id
        assert kw['name'] == name
        assert kw['order'] == order
        assert kw['moduleID'] == module_id

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.Module.from_json")
    def test_module_not_found(self, mock_from_json, mock_new_client):
        mock_client = mock.MagicMock()
        mock_post = mock.MagicMock()
        mock_client.post.return_value = mock_post
        mock_new_client.return_value = mock_client
        mock_module = mock.MagicMock()
        case_id, model_id, module_id, name, order = 'c', 'm', 'mi', 'n', 'o'
        fake_line_item = FakeLineItem(name='garbage')
        mock_module.line_items = [fake_line_item]
        mock_from_json.return_value = mock_module
        with pytest.raises(AddLineItemException) as err:
            Modeling.add_line_item(case_id, model_id, module_id, name, order)
        assert name in str(err)


class TestNewModelGroups:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.ModelGroups.from_json")
    def test_works_ok(self, mock_from_json, mock_new_client):
        group_name = 'groupName'
        count_model_ids = 2
        model_ids = valid_uids(count_model_ids)
        mock_client = mock.MagicMock()
        mock_new_model_groups_data = mock.MagicMock()
        mock_new_client.return_value = mock_client
        mock_client.post.return_value = mock_new_model_groups_data
        nmg = Modeling.new_model_groups(group_name, model_ids)
        mock_new_client.assert_called_once()
        mock_client.post.assert_called_once()
        _, kww = mock_client.post.call_args
        sent_data = kww.get('data')
        assert 'name' in sent_data
        assert sent_data['name'] == group_name
        assert 'modelIDs' in sent_data
        assert sent_data['modelIDs'] == model_ids
        mock_from_json.assert_called_once()

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises(self, mock_new_client):
        group_name = 'groupName'
        count_model_ids = 2
        model_ids = valid_uids(count_model_ids)
        mock_client = mock.MagicMock()
        mock_new_client.return_value = mock_client
        mock_client.post.side_effect = Exception
        with pytest.raises(Exception):
            nmg = Modeling.new_model_groups(group_name, model_ids)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises_ModelingServicePostException(self, mock_new_client):
        group_name = 'groupName'
        count_model_ids = 2
        model_ids = valid_uids(count_model_ids)
        mock_client = mock.MagicMock()
        err_data, err_code, err_url = 42, 400, 'http://www.'

        mock_new_client.return_value = mock_client
        mock_client.post.side_effect = ModelingServicePostException(
            err_data, err_code, err_url)
        with pytest.raises(NewModelGroupsException) as err:
            Modeling.new_model_groups(group_name, model_ids)
        assert "error adding new model groups" in str(err)


class TestDynamicUpdates:

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_works_ok(self, mock_new_socket_client):
        mock_client = mock.MagicMock()
        fake_return_data = 42
        mock_client.get.return_value = fake_return_data
        mock_new_socket_client.return_value = mock_client
        d = Modeling.dynamic_updates()
        mock_new_socket_client.assert_called_once()
        assert d == fake_return_data
        _, kww = mock_client.get.call_args
        assert kww.get('data').get(
            'action') == Modeling.ModelingActions.DYNAMIC_UPDATES
        assert 'username' in kww.get('data')
        assert 'password' in kww.get('data')


class TestPullModelGroups:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.ModelGroups.from_json")
    def test_works_ok(self, mock_from_json, mock_new_client):
        mock_client = mock.MagicMock()
        fake_return_data = mock.MagicMock()

        mock_client.get.return_value = fake_return_data
        mock_new_client.return_value = mock_client
        pmg = Modeling.pull_model_groups()
        mock_client.get.assert_called_once()
        mock_from_json.assert_called_once_with(fake_return_data.get('data'))

    @pytest.mark.parametrize('success_response', [{
        'data': []
    }, {
        'data': None
    }, {
        'data': [{}, {}]
    }])
    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok_various_data_empty(self, mock_new_client,
                                         success_response):
        mock_c = mock.MagicMock()
        mock_c.get.return_value = success_response
        mock_new_client.return_value = mock_c
        mg = Modeling.pull_model_groups()
        mock_c.get.assert_called_once_with(url=VSURL.USERS_GROUPS)
        assert isinstance(mg, ModelGroups)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok_with_group(self, mock_new_client):
        mock_c = mock.MagicMock()
        success_response = {
            'data': [{
                ModelGroup.fields.UID: '42',
                ModelGroup.fields.NAME: "name",
                ModelGroup.fields.USER_ID: 'user',
                ModelGroup.fields.MODEL_IDS: ['41', '42']
            }]
        }
        mock_c.get.return_value = success_response
        mock_new_client.return_value = mock_c
        mg = Modeling.pull_model_groups()
        mock_c.get.assert_called_once_with(url=VSURL.USERS_GROUPS)
        assert len(mg.groups) == 1
        assert mg.groups[0].uid == '42'
        assert mg.groups[0].name == 'name'
        assert mg.groups[0].user_id == 'user'
        assert mg.groups[0].model_ids == ['41', '42']

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_get_raises(self, mock_new_client):
        mock_client = mock.MagicMock()
        mock_new_client.return_value = mock_client

        err_data, err_code, err_url = 42, 400, 'http://www.'
        mock_client.get.side_effect = ModelingServiceGetException(
            err_data, err_code, err_url)
        with pytest.raises(PullModelGroupsException) as err:
            Modeling.pull_model_groups()
        assert str(err_data) in str(err)
        assert str(err_code) in str(err)
        assert err_url in str(err)


class TestUpdateModelGroups:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.ModelGroups.from_json")
    def test_works_ok(self, mock_from_json, mock_new_client):
        uid, name, model_ids = valid_uid(), 'groupName', ['02x', '03x']
        mock_client = mock.MagicMock()
        fake_return_data = mock.MagicMock()

        mock_client.post.return_value = fake_return_data
        mock_new_client.return_value = mock_client
        pmg = Modeling.update_model_groups(uid, name, model_ids)
        mock_client.post.assert_called_once()
        mock_from_json.assert_called_once_with(fake_return_data.get('data'))

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_post_raises(self, mock_new_client):
        mock_client = mock.MagicMock()
        mock_new_client.return_value = mock_client
        uid, name, model_ids = valid_uid(), 'groupName', ['02x', '03x']
        err_data, err_code, err_url = 42, 400, 'http://www.'
        mock_client.post.side_effect = ModelingServicePostException(
            err_data, err_code, err_url)
        with pytest.raises(UpdateModelGroupsException) as err:
            Modeling.update_model_groups(uid, name, model_ids)
        assert str(err_data) in str(err)
        assert str(err_code) in str(err)
        assert err_url in str(err)


class TestTagLineItem:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.LineItem.from_json")
    def test_works_ok(self, mock_from_json, mock_new_client):
        model_id = valid_uid()
        line_item_id = valid_uid()
        tags = valid_tags()
        fake_return_data = mock.MagicMock()

        mock_client = mock.MagicMock()
        mock_client.post.return_value = fake_return_data

        mock_new_client.return_value = mock_client
        tli = Modeling.tag_line_item(model_id, line_item_id, tags)

        mock_new_client.assert_called_once()
        _, kw = mock_client.post.call_args
        assert 'data' in kw
        assert kw.get('data').get('lineItemId') == line_item_id
        assert kw.get('data').get('modelID') == model_id
        assert kw.get('data').get('tags') == tags

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises(self, mock_new_client):
        model_id = valid_uid()
        line_item_id = valid_uid()
        tags = valid_tags()
        d, s, u = 42, 4, 'www'

        mock_client = mock.MagicMock()
        mock_client.post.side_effect = ModelingServicePostException(d, s, u)

        mock_new_client.return_value = mock_client
        with pytest.raises(TagLineItemException) as err:
            Modeling.tag_line_item(model_id, line_item_id, tags)
        assert 'error tagging line item' in str(err)


class TestShareModel:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok_no_auth_token(self, mock_new_client):
        model_id = valid_uid()

        email, permission = 'e', valid_permission()
        fake_return_data = mock.MagicMock()

        mock_client = mock.MagicMock()
        mock_client.post.return_value = fake_return_data

        mock_new_client.return_value = mock_client
        Modeling.share_model(model_id, email, permission.permission)

        mock_new_client.assert_called_once()
        _, kw = mock_client.post.call_args
        assert kw.get('headers').get('email') == email
        assert kw.get('headers').get('modelID') == model_id
        assert kw.get('data') == permission.jsonify()

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises(self, mock_new_client):
        model_id = valid_uid()

        email, permission = valid_email(), valid_permission()

        mock_client = mock.MagicMock()
        d, s, u = 42, 4, 'www'

        mock_client.post.side_effect = ModelingServicePostException(d, s, u)

        mock_new_client.return_value = mock_client
        with pytest.raises(ShareModelException) as err:
            Modeling.share_model(model_id, email, permission.permission)
        assert 'failed to share models' in str(err)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_bad_permission(self, mock_new_client):
        model_id = valid_uid()

        email, permission = valid_email(), 'garbagge'

        mock_client = mock.MagicMock()

        mock_new_client.return_value = mock_client
        with pytest.raises(NotImplementedError) as err:
            Modeling.share_model(model_id, email, permission)
        assert permission in str(err)


class TestPullModelDatasources:

    @mock.patch(f"{MODULE_PREFIX}.pull_model_information")
    def test_works_ok(self, mock_pull_model_information):
        model_id = valid_uid()
        mock_ds = mock.MagicMock()
        mock_pull_model_information.return_value.data_sources = mock_ds
        assert Modeling.pull_model_datasources(model_id) == mock_ds
        mock_pull_model_information.assert_called_once_with(model_id)


class TestGetModelTags:

    @mock.patch(f"{MODULE_PREFIX}.pull_model_information")
    def test_works_ok(self, mock_pull_model_information):
        uid = valid_uid()
        mock_tags = mock.MagicMock()
        mock_pull_model_information.return_value.tags = mock_tags
        assert Modeling.get_model_tags(uid) == mock_tags
        mock_pull_model_information.assert_called_once_with(uid)


class TestAppendlTags:

    @mock.patch(f"{MODULE_PREFIX}.tag_model")
    @mock.patch(f"{MODULE_PREFIX}.get_model_tags")
    def test_works_ok(self, mock_get_model_tags, mock_tag_model):
        uid = valid_uid()
        tags = valid_tags(count=5)
        mock_get_model_tags.return_value = valid_tags(count=2)
        Modeling.append_tags(uid, tags)
        a, _ = mock_tag_model.call_args
        mock_tag_model.assert_called_once
        call_uid, tags = a[0], a[1]
        assert call_uid == uid
        assert len(tags) == 5 + 2

    @mock.patch(f"{MODULE_PREFIX}.tag_model")
    @mock.patch(f"{MODULE_PREFIX}.get_model_tags")
    def test_works_ensure_union(self, mock_get_model_tags, mock_tag_model):
        uid = valid_uid()
        tags = valid_tags(count=5)
        mock_get_model_tags.return_value = tags
        Modeling.append_tags(uid, tags)
        a, _ = mock_tag_model.call_args
        mock_tag_model.assert_called_once
        call_uid, tags = a[0], a[1]
        assert call_uid == uid
        assert len(tags) == 5


class TestRecalculateModel:

    @property
    def success_response(self):
        return {
            'status': Vars.SUCCESS,
            "data": {
                "facts": [{
                    "id": "161396b0-5f43-4d20-ab82-94b291974d81",
                    "identifier":
                    "[Cash Flow From Financing Activities[Repayments of long term debt[2018]]]",
                    "period": 2018,
                    "format": "{}",
                    "value": "-0",
                    "dataValue": "-0",
                    "formula": "-0",
                    "internalFormula": "-0",
                    "edges": {
                        "dependantCells": [{
                            "id": "f6390bf9-49f4-451d-b339-d63d98c944ac",
                            "identifier":
                            "[Cash Flow statement[Repayments of long term debt[2018]]]",
                            "edges": {}
                        }]
                    }
                }]
            }
        }

    @property
    def failed_response(self):
        return {'status': 'garbage'}

    @mock.patch(f"{MODULE_PREFIX}.facts_list")
    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok(self, mock_new_client, mock_facts_list):
        model_id = valid_uid()
        mock_c = mock.MagicMock()
        mock_new_client.return_value = mock_c
        mock_c.post.return_value = self.success_response
        mfl = mock_facts_list.return_value
        assert Modeling.recalculate_model(model_id) == mfl
        _, kw = mock_c.post.call_args
        assert 'url' in kw
        assert kw.get('data').get(Headers.MODEL_ID) == model_id
        mock_facts_list.assert_called_once()

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises_not_success(self, mock_new_client):
        model_id = valid_uid()
        mock_c = mock.MagicMock()
        mock_new_client.return_value = mock_c
        mock_c.post.return_value = self.failed_response
        with pytest.raises(RecalculateModelException) as err:
            Modeling.recalculate_model(model_id)
        assert 'recalculating model' in str(err)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises_post_exception(self, mock_new_client):
        model_id = valid_uid()
        mock_c = mock.MagicMock()
        mock_new_client.return_value = mock_c
        mock_c.post.side_effect = ModelingServicePostException('d', 4, 'www')
        with pytest.raises(RecalculateModelException) as err:
            Modeling.recalculate_model(model_id)
        assert 'recalculating model' in str(err)


class TestRemoveModule:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok(self, mock_new_client):
        model_id = valid_uid()

        module_id = valid_uid()

        mock_c = mock.MagicMock()
        mock_c.post.return_value = {'status': 'success'}
        mock_new_client.return_value = mock_c
        assert Modeling.remove_module(model_id, module_id)
        mock_c.post.assert_called_once()
        _, kw = mock_c.post.call_args
        assert kw.get('data') == {
            Headers.MODEL_ID: model_id,
            Headers.MODULE_ID: module_id,
        }

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises(self, mock_new_client):
        model_id = valid_uid()

        module_id = valid_uid()

        mock_c = mock.MagicMock()
        d, s, u = 42, 4, 'www'
        mock_c.post.side_effect = ModelingServicePostException(d, s, u)
        mock_new_client.return_value = mock_c
        with pytest.raises(RemoveModuleException) as err:
            Modeling.remove_module(model_id, module_id)
        assert 'error removing module' in str(err)


class TestAddChildModule:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.Module.from_json")
    def test_works_ok(self, mock_from_json, mock_new_client):
        parent_module_id = valid_uid()
        name = valid_name()
        model_id = valid_uid()
        case_id = valid_uid()
        mock_c = mock.MagicMock()
        mock_new_mod = mock.MagicMock()
        mock_new_client.return_value = mock_c
        mock_from_json.return_value = mock_new_mod
        module = {'name': name, 'thing': 42}
        mock_c.post.return_value = {
            'data': {
                'module': {
                    'edges': {
                        'childModules': [module]
                    }
                }
            }
        }
        assert Modeling.add_child_module(parent_module_id, name, model_id,
                                         case_id) == mock_new_mod
        mock_from_json.assert_called_once_with(module)
        _, kw = mock_c.post.call_args
        assert 'url' in kw
        assert kw.get('data') == {
            Headers.CASE_ID: case_id,
            Headers.MODEL_ID: model_id,
            Headers.NAME: name,
            Headers.PARENT_MODULE_ID: parent_module_id,
        }

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok_module_not_found(self, mock_new_client):
        parent_module_id = valid_uid()
        name = valid_name()
        model_id = valid_uid()
        case_id = valid_uid()
        mock_c = mock.MagicMock()

        mock_new_client.return_value = mock_c

        mock_c.post.return_value = {
            'data': {
                'module': {
                    'edges': {
                        'childModules': [{
                            'name': 'any',
                            'thing': 42
                        }]
                    }
                }
            }
        }
        with pytest.raises(AddChildModuleException) as err:
            Modeling.add_child_module(parent_module_id, name, model_id,
                                      case_id)
        assert f' could not find module with name {name}' in str(err)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_incorrect_data_structure(self, mock_new_client):
        parent_module_id = valid_uid()
        name = valid_name()
        model_id = valid_uid()
        case_id = valid_uid()
        mock_c = mock.MagicMock()

        mock_new_client.return_value = mock_c

        mock_c.post.return_value = {'data': {}}
        with pytest.raises(AddChildModuleException) as err:
            Modeling.add_child_module(parent_module_id, name, model_id,
                                      case_id)
        assert 'Error adding child module: unexpected data structure' in str(
            err)


class TestAddLineItem:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok(self, mock_new_client):
        case_id = valid_uid()
        model_id = valid_uid()
        module_id = valid_uid()
        name = valid_name()
        order = 1

        mock_c = mock.MagicMock()
        mock_new_client.return_value = mock_c

        expected_line_item_data = {'id': '0x2', 'name': name, 'facts': []}

        mock_c.post.return_value = {
            'data': {
                'module': {
                    "edges": {
                        'lineItems': [expected_line_item_data]
                    }
                }
            }
        }
        rl = Modeling.add_line_item(case_id, model_id, module_id, name, order)
        assert rl.name == name
        assert rl.uid == expected_line_item_data.get('id')

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_bad_data(self, mock_new_client):
        case_id = valid_uid()
        model_id = valid_uid()
        module_id = valid_uid()
        name = valid_name()
        order = 1

        mock_c = mock.MagicMock()
        mock_new_client.return_value = mock_c

        mock_c.post.return_value = {'data': {}}
        with pytest.raises(AddLineItemException) as err:
            Modeling.add_line_item(case_id, model_id, module_id, name, order)
        assert 'error adding line item: invalid data structure' in str(err)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_cant_find_line_item(self, mock_new_client):
        case_id = valid_uid()
        model_id = valid_uid()
        module_id = valid_uid()
        name = valid_name()
        order = 1

        mock_c = mock.MagicMock()
        mock_new_client.return_value = mock_c

        expected_line_item_data = {
            'uid': '0x2',
            'name': 'somethingElse',
            'facts': []
        }

        mock_c.post.return_value = {
            'data': {
                'module': {
                    'edges': {
                        'lineItems': [expected_line_item_data]
                    }
                }
            }
        }
        with pytest.raises(AddLineItemException) as err:
            Modeling.add_line_item(case_id, model_id, module_id, name, order)
        assert f'error adding line item: cannot find module with name {name}' in str(
            err)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_client_raises(self, mock_new_client):
        case_id = valid_uid()
        model_id = valid_uid()
        module_id = valid_uid()
        name = valid_name()
        order = 1

        mock_c = mock.MagicMock()
        mock_new_client.return_value = mock_c
        d, s, u = 42, 4, 'www'
        mock_c.post.side_effect = ModelingServicePostException(d, s, u)
        with pytest.raises(AddLineItemException) as err:
            Modeling.add_line_item(case_id, model_id, module_id, name, order)
        assert 'error adding line item' in str(err)
        assert model_id in str(err)
        assert module_id in str(err)


class TestEditFacts:

    @property
    def success_response(self):
        return {
            'status': Vars.SUCCESS,
            "data": {
                "facts": [{
                    "id": "161396b0-5f43-4d20-ab82-94b291974d81",
                    "identifier":
                    "[Cash Flow From Financing Activities[Repayments of long term debt[2018]]]",
                    "period": 2018,
                    "format": "{}",
                    "value": "-0",
                    "dataValue": "-0",
                    "formula": "-0",
                    "internalFormula": "-0",
                    "edges": {
                        "dependantCells": [{
                            "id": "f6390bf9-49f4-451d-b339-d63d98c944ac",
                            "identifier":
                            "[Cash Flow statement[Repayments of long term debt[2018]]]",
                            "edges": {}
                        }]
                    }
                }]
            }
        }

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok(self, mock_new_client):
        url = 'www'
        case_id = valid_uid()
        model_id = valid_uid()
        facts = [1, 2, 3]
        mock_c = mock.MagicMock()
        mock_c.post.return_value = self.success_response
        mock_new_client.return_value = mock_c
        Modeling.edit_facts(url, case_id, model_id, facts)
        mock_new_client.assert_called_once()
        mock_c.post.assert_called_once
        _, kw = mock_c.post.call_args
        assert kw.get('url') == url
        assert kw.get('data') == {
            Headers.CASE_ID: case_id,
            Headers.MODEL_ID: model_id,
            "forecastIncrement": 1,
            "facts": facts,
        }


class TestEditFormat:

    @mock.patch(f"{MODULE_PREFIX}.edit_facts")
    def test_works_ok(self, mock_edit_facts):
        case_id = valid_uid()
        model_id = valid_uid()
        facts = [1, 2, 3]
        Modeling.edit_format(case_id, model_id, facts)
        mock_edit_facts.assert_called_once()
        _, kw = mock_edit_facts.call_args
        assert kw.get('case_id') == case_id
        assert kw.get('model_id') == model_id
        assert kw.get('facts') == facts


class TestEditFormula:

    @mock.patch(f"{MODULE_PREFIX}.edit_facts")
    def test_works_ok(self, mock_edit_facts):
        case_id = valid_uid()
        model_id = valid_uid()
        facts = [1, 2, 3]
        Modeling.edit_formula(case_id, model_id, facts)
        mock_edit_facts.assert_called_once()
        _, kw = mock_edit_facts.call_args
        assert kw.get('case_id') == case_id
        assert kw.get('model_id') == model_id
        assert kw.get('facts') == facts
