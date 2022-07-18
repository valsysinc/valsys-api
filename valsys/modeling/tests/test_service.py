from dataclasses import dataclass
from valsys.modeling.service import pull_model_information, pull_case, spawn_model, add_line_item, CREATE_MODEL_ACTION
from valsys.modeling.client.service import ModelingClientTypes
import pytest
from unittest import mock
from valsys.spawn.exceptions import ModelSpawnException

MODULE_PREFIX = "valsys.modeling.service"


class TestSpawnModel:

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_works_ok(self, mock_new_socket_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        auth_token = '1234'
        fake_post_ret = {'data': {'uid': 42}}
        mock_c.post.return_value = fake_post_ret
        mock_new_socket_client.return_value = mock_c

        assert spawn_model(config,
                           auth_token) == fake_post_ret.get('data').get('uid')
        assert config.action == CREATE_MODEL_ACTION
        config.validate.assert_called_once()
        config.jsonify.assert_called_once()
        mock_new_socket_client.assert_called_with(auth_token=auth_token)


class TestPullModelInformation:

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
        with pytest.raises(ValueError) as err:
            add_line_item(case_id, model_id, module_id, name, order)
        assert name in str(err)
