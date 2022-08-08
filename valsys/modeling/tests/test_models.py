import pytest

from valsys.modeling.models import ModelGroup, PermissionTypes, Permissions


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
