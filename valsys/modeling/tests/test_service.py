from valsys.modeling.service import pull_model_information, pull_case, spawn_model
from valsys.modeling.client.service import ModelingClientTypes
import pytest
from unittest import mock
from valsys.spawn.exceptions import ModelSpawnException

MODULE_PREFIX = "valsys.modeling.service"


class TestSpawnModel:
    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok(self, mock_new_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        auth_token = '1234'
        mock_c.get.return_value = {'data': {'uid': 42}}
        mock_new_client.return_value = mock_c

        assert spawn_model(config, auth_token) == 42
        assert config.action == 'CREATE_MODEL'
        config.validate.assert_called_once()
        config.jsonify.assert_called_once()
        mock_new_client.assert_called_with(auth_token=auth_token, client=ModelingClientTypes.SOCKET)


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
