import pytest

from valsys.modeling.models import PermissionTypes, Permissions


class TestPermissions:

    @pytest.mark.parametrize("permission", PermissionTypes.types())
    def test_works_ok(self, permission):
        p = Permissions(permission)
        assert p.jsonify() == {permission: True}
