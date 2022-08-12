from dataclasses import dataclass
from unittest import mock

import pytest

from valsys.modeling.client.exceptions import ModelingServiceGetException
from valsys.modeling.exceptions import (
    AddLineItemException,
    PullModelGroupsException,
)
from valsys.modeling.service import (ModelingActions, SpawnedModelInfo,
                                     add_line_item, dynamic_updates,
                                     new_model_groups, pull_case,
                                     pull_model_groups, pull_model_information,
                                     spawn_model, update_model_groups)
from valsys.spawn.exceptions import ModelSpawnException

MODULE_PREFIX = "valsys.modeling.service"


class TestSpawnModel:

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_works_ok(self, mock_new_socket_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        fake_model_id, fake_model_ticker = 'ghjkrhdg', 'TKR'
        fake_post_ret = {
            'models': [{
                'modelID': fake_model_id,
                'status': 'success',
                'ticker': fake_model_ticker
            }]
        }
        mock_c.post.return_value = fake_post_ret
        mock_new_socket_client.return_value = mock_c

        assert spawn_model(config) == [
            SpawnedModelInfo(model_id=fake_model_id, ticker=fake_model_ticker)
        ]
        assert config.action == ModelingActions.SPAWN_MODELS

        config.jsonify.assert_called_once()
        mock_new_socket_client.assert_called_once()

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_works_ok_no_success(self, mock_new_socket_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        fake_model_id, fake_model_ticker = 'ghjkrhdg', 'TKR'
        fake_post_ret = {
            'models': [{
                'modelID': fake_model_id,
                'status': 'garbage',
                'ticker': fake_model_ticker
            }]
        }
        mock_c.post.return_value = fake_post_ret
        mock_new_socket_client.return_value = mock_c

        assert spawn_model(config) == []
        assert config.action == ModelingActions.SPAWN_MODELS

        config.jsonify.assert_called_once()
        mock_new_socket_client.assert_called_once()

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_raises(self, mock_new_socket_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        data, code, url = 42, 1, 'www'
        mock_c.post.side_effect = ModelingServiceGetException(data, code, url)
        mock_new_socket_client.return_value = mock_c
        with pytest.raises(ModelSpawnException) as err:
            spawn_model(config)
        assert 'error building model' in str(err)
        assert str(data) in str(err)
        assert str(code) in str(err)
        assert url in str(err)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.ModelInformation.from_json")
    def test_works_ok(self, mock_ModelInformation_from_json, mock_new_client):
        uid = '1234'
        mock_get = mock.MagicMock()
        mock_cases = mock.MagicMock()
        mock_model_info = mock.MagicMock()
        mock_get.return_value = {'data': {'model': mock_cases}}
        mock_new_client.return_value.get = mock_get
        mock_ModelInformation_from_json.return_value = mock_model_info
        model_info = pull_model_information(uid)
        mock_new_client.assert_called_once()
        mock_get.assert_called_once()
        _, kw = mock_get.call_args
        assert kw.get('headers') == {'modelID': uid}
        mock_ModelInformation_from_json.assert_called_once_with(
            uid, mock_cases)
        assert model_info == mock_model_info


class TestPullCase:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.Case.from_json")
    def test_works_ok(self, mock_Case_from_json, mock_new_client):
        uid = '1234'
        mock_get = mock.MagicMock()
        mock_cases = mock.MagicMock()
        mock_model_info = mock.MagicMock()
        mock_get.return_value = {'data': {'case': mock_cases}}
        mock_new_client.return_value.get = mock_get
        mock_Case_from_json.return_value = mock_model_info
        model_info = pull_case(uid)
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
        mock_post = mock.MagicMock()
        mock_client.post.return_value = mock_post
        mock_new_client.return_value = mock_client
        mock_module = mock.MagicMock()
        case_id, model_id, module_id, name, order = 'c', 'm', 'mi', 'n', 'o'
        fake_line_item = FakeLineItem(name=name)
        mock_module.line_items = [fake_line_item]
        mock_from_json.return_value = mock_module

        li = add_line_item(case_id, model_id, module_id, name, order)
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
            add_line_item(case_id, model_id, module_id, name, order)
        assert name in str(err)


class TestAddNewModelGroups:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.ModelGroups.from_json")
    def test_works_ok(self, mock_from_json, mock_new_client):
        group_name = 'groupName'
        model_ids = ['1', '2']
        mock_client = mock.MagicMock()
        mock_new_model_groups_data = mock.MagicMock()
        mock_new_client.return_value = mock_client
        mock_client.post.return_value = mock_new_model_groups_data
        nmg = new_model_groups(group_name, model_ids)
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
        model_ids = ['1', '2']
        mock_client = mock.MagicMock()
        mock_new_client.return_value = mock_client
        mock_client.post.side_effect = Exception
        with pytest.raises(Exception):
            nmg = new_model_groups(group_name, model_ids)


class TestDynamicUpdates:

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_works_ok(self, mock_new_socket_client):
        mock_client = mock.MagicMock()
        fake_return_data = 42
        mock_client.get.return_value = fake_return_data
        mock_new_socket_client.return_value = mock_client
        d = dynamic_updates()
        mock_new_socket_client.assert_called_once()
        assert d == fake_return_data
        _, kww = mock_client.get.call_args
        assert kww.get('data').get('action') == ModelingActions.DYNAMIC_UPDATES
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
        pmg = pull_model_groups()
        mock_client.get.assert_called_once()
        mock_from_json.assert_called_once_with(fake_return_data.get('data'))

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_get_raises(self, mock_new_client):
        mock_client = mock.MagicMock()
        mock_new_client.return_value = mock_client

        err_data, err_code, err_url = 42, 400, 'http://www.'
        mock_client.get.side_effect = ModelingServiceGetException(
            err_data, err_code, err_url)
        with pytest.raises(PullModelGroupsException) as err:
            pull_model_groups()
        assert str(err_data) in str(err)
        assert str(err_code) in str(err)
        assert err_url in str(err)


class TestUpdateModelGroups:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.ModelGroups.from_json")
    def test_works_ok(self, mock_from_json, mock_new_client):
        uid, name, model_ids = '01x', 'groupName', ['02x', '03x']
        mock_client = mock.MagicMock()
        fake_return_data = mock.MagicMock()

        mock_client.post.return_value = fake_return_data
        mock_new_client.return_value = mock_client
        pmg = update_model_groups(uid, name, model_ids)
        mock_client.post.assert_called_once()
        mock_from_json.assert_called_once_with(fake_return_data.get('data'))
