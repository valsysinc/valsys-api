import json
from ..service import tag_models, share_model, delete_models, CODE_POST_SUCCESS
from unittest import mock
from valsys.config import URL_MODELING_MODEL_PROPERTIES, URL_USERS_SHARE_MODEL, URL_USERS_MODELS
MODULE_PREFIX = 'valsys.modeling.service'


class TestTagModels:
    @mock.patch(
        f"{MODULE_PREFIX}.requests.post"
    )
    def test_tag(self, mock_post):
        model_id, tags, auth_token = 'mid', 'tags', 'at'
        mock_post.return_value.status_code = CODE_POST_SUCCESS
        tag_models(model_id, tags, auth_token)
        mock_post.assert_called_with(
            url=URL_MODELING_MODEL_PROPERTIES,
            headers={'content-type': 'application/json', 'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({"modelID": model_id, "modelTags": tags, "update": True, "rollForward": True}))


class TestShareModel:
    @mock.patch(
        f"{MODULE_PREFIX}.requests.post"
    )
    def test_share_view(self, mock_post):
        model_id, user_email, permission, auth_token = 'mid', 'me@you', 'view', 'at'
        mock_post.return_value.status_code = CODE_POST_SUCCESS
        share_model(model_id, user_email, permission, auth_token)
        mock_post.assert_called_with(
            url=URL_USERS_SHARE_MODEL,
            headers={'content-type': 'application/json', 'Authorization': f'Bearer {auth_token}', "email": user_email,
                     "modelID": model_id},
            data=json.dumps({
                "view": True,
            }))

    @mock.patch(
        f"{MODULE_PREFIX}.requests.post"
    )
    def test_share_edit(self, mock_post):
        model_id, user_email, permission, auth_token = 'mid', 'me@you', 'garbage', 'at'
        mock_post.return_value.status_code = CODE_POST_SUCCESS
        share_model(model_id, user_email, permission, auth_token)
        mock_post.assert_called_with(
            url=URL_USERS_SHARE_MODEL,
            headers={'content-type': 'application/json', 'Authorization': f'Bearer {auth_token}', "email": user_email,
                     "modelID": model_id},
            data=json.dumps({
                "edit": True,
            }))


class TestDeleteModels:
    @mock.patch(
        f"{MODULE_PREFIX}.requests.delete"
    )
    def test_delete_ok(self, mock_delete):
        model_id_lst, auth_token = 'models', 'at'

        delete_models(model_id_lst, auth_token)
        mock_delete.assert_called_with(url=URL_USERS_MODELS,
                                       headers={'content-type': 'application/json',
                                                'Authorization': f'Bearer {auth_token}'},
                                       data=json.dumps({"models": model_id_lst}))
