from valsys.modeling.models import Permissions, PermissionTypes
import pytest


class TestPermissions:

    @pytest.mark.parametrize("permission", PermissionTypes.types())
    def test_works_ok(self, permission):
        p = Permissions(permission)
        assert p.jsonify() == {permission: True}
