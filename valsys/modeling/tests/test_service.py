from dataclasses import dataclass
from unittest import mock

import pytest

from valsys.modeling.client.exceptions import (
    ModelingServiceGetException,
    ModelingServicePostException,
)
from valsys.modeling.exceptions import (
    AddLineItemException, PullModelGroupsException, ShareModelException,
    UpdateModelGroupsException, TagLineItemException, TagModelException,
    NewModelGroupsException, PullModelInformationException)
from valsys.modeling.service import (
    ModelingActions, SpawnedModelInfo, add_line_item, dynamic_updates,
    new_model_groups, pull_case, pull_model_groups, pull_model_information,
    share_model, spawn_model, tag_line_item, tag_model, update_model_groups,
    pull_model_datasources, get_model_tags, append_tags)
from valsys.spawn.exceptions import ModelSpawnException

from .factories import (
    valid_email,
    valid_permission,
    valid_tags,
    valid_ticker,
    valid_uid,
    valid_uids,
)

MODULE_PREFIX = "valsys.modeling.service"


class TestSpawnModel:

    @mock.patch(f"{MODULE_PREFIX}.new_socket_client")
    def test_works_ok(self, mock_new_socket_client):
        config = mock.MagicMock()
        mock_c = mock.MagicMock()
        fake_model_id, fake_model_ticker = valid_uid(), valid_ticker()
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
        fake_model_id, fake_model_ticker = 'ghjkrhdg', valid_ticker()
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


class TestPullModelInformation:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.ModelInformation.from_json")
    def test_works_ok_frm_json(self, mock_ModelInformation_from_json,
                               mock_new_client):
        uid = valid_uid()
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

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_raises(self, mock_new_client):
        mock_c = mock.MagicMock()
        d, c, u = 42, 42, 'www'
        mock_c.get.side_effect = ModelingServiceGetException(d, c, u)
        mock_new_client.return_value = mock_c
        model_id = valid_uid(), valid_tags()
        with pytest.raises(PullModelInformationException) as err:
            pull_model_information(model_id)
        assert 'could not pull model info for model' in str(err)


class TestTagModel:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok_without_auth_token(self, mock_new_client):

        mock_c = mock.MagicMock()
        mock_post_ret = mock.MagicMock()

        mock_c.post.return_value = mock_post_ret
        mock_new_client.return_value = mock_c
        model_id, tags = valid_uid(), valid_tags()
        assert tag_model(model_id, tags) == mock_post_ret

        mock_new_client.assert_called_once_with(None)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_works_ok_with_auth_token(self, mock_new_client):

        mock_c = mock.MagicMock()
        mock_post_ret = mock.MagicMock()

        mock_c.post.return_value = mock_post_ret
        mock_new_client.return_value = mock_c
        model_id, tags, auth_token = valid_uid(), valid_tags(), 't0k3n'
        assert tag_model(model_id, tags,
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
            tag_model(model_id, tags)
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
        count_model_ids = 2
        model_ids = valid_uids(count_model_ids)
        mock_client = mock.MagicMock()
        mock_new_client.return_value = mock_client
        mock_client.post.side_effect = Exception
        with pytest.raises(Exception):
            nmg = new_model_groups(group_name, model_ids)

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
            new_model_groups(group_name, model_ids)
        assert "error adding new model groups" in str(err)


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
        uid, name, model_ids = valid_uid(), 'groupName', ['02x', '03x']
        mock_client = mock.MagicMock()
        fake_return_data = mock.MagicMock()

        mock_client.post.return_value = fake_return_data
        mock_new_client.return_value = mock_client
        pmg = update_model_groups(uid, name, model_ids)
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
            update_model_groups(uid, name, model_ids)
        assert str(err_data) in str(err)
        assert str(err_code) in str(err)
        assert err_url in str(err)


class TestTagLineItem:

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    @mock.patch(f"{MODULE_PREFIX}.TaggedLineItemResponse.from_json")
    def test_works_ok(self, mock_from_json, mock_new_client):
        model_id = valid_uid()
        line_item_id = valid_uid()
        tags = valid_tags()
        fake_return_data = mock.MagicMock()

        mock_client = mock.MagicMock()
        mock_client.post.return_value = fake_return_data

        mock_new_client.return_value = mock_client
        tli = tag_line_item(model_id, line_item_id, tags)

        mock_new_client.assert_called_once()
        _, kw = mock_client.post.call_args
        assert 'data' in kw
        assert kw.get('data').get('uid') == line_item_id
        assert kw.get('data').get('modelID') == model_id
        assert kw.get('data').get('tags') == tags
        mock_from_json.assert_called_once_with(
            fake_return_data.get('data').get('lineItems')[0])

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
            tag_line_item(model_id, line_item_id, tags)
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
        share_model(model_id, email, permission.permission)

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
            share_model(model_id, email, permission.permission)
        assert 'failed to share models' in str(err)

    @mock.patch(f"{MODULE_PREFIX}.new_client")
    def test_bad_permission(self, mock_new_client):
        model_id = valid_uid()

        email, permission = valid_email(), 'garbagge'

        mock_client = mock.MagicMock()

        mock_new_client.return_value = mock_client
        with pytest.raises(NotImplementedError) as err:
            share_model(model_id, email, permission)
        assert permission in str(err)


class TestPullModelDatasources:

    @mock.patch(f"{MODULE_PREFIX}.pull_model_information")
    def test_works_ok(self, mock_pull_model_information):
        model_id = valid_uid()
        mock_ds = mock.MagicMock()
        mock_pull_model_information.return_value.data_sources = mock_ds
        assert pull_model_datasources(model_id) == mock_ds
        mock_pull_model_information.assert_called_once_with(model_id)


class TestGetModelTags:

    @mock.patch(f"{MODULE_PREFIX}.pull_model_information")
    def test_works_ok(self, mock_pull_model_information):
        uid = valid_uid()
        mock_tags = mock.MagicMock()
        mock_pull_model_information.return_value.tags = mock_tags
        assert get_model_tags(uid) == mock_tags
        mock_pull_model_information.assert_called_once_with(uid)


class TestAppendlTags:

    @mock.patch(f"{MODULE_PREFIX}.tag_model")
    @mock.patch(f"{MODULE_PREFIX}.get_model_tags")
    def test_works_ok(self, mock_get_model_tags, mock_tag_model):
        uid = valid_uid()
        tags = valid_tags(count=5)
        mock_get_model_tags.return_value = valid_tags(count=2)
        append_tags(uid, tags)
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
        append_tags(uid, tags)
        a, _ = mock_tag_model.call_args
        mock_tag_model.assert_called_once
        call_uid, tags = a[0], a[1]
        assert call_uid == uid
        assert len(tags) == 5
