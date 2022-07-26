from typing import Dict


class PermissionTypes:
    VIEW = 'view'
    EDIT = 'edit'
    FULL_ACCESS = 'fullAccess'

    @classmethod
    def types(cls):
        return [cls.VIEW, cls.EDIT, cls.FULL_ACCESS]

    @classmethod
    def valid(cls, p):
        return p in cls.types()


class Permissions:

    def __init__(self, permission: str):
        self.permission = permission

    def jsonify(self) -> Dict[str, bool]:
        """Generate a permissions body from the
        provided permissions string.
        
        If an invalid permission string is
        given, a `NotImplementedError` is thrown."""
        if self.permission == PermissionTypes.VIEW:
            return {
                PermissionTypes.VIEW: True,
            }
        elif self.permission == PermissionTypes.EDIT:
            return {
                PermissionTypes.EDIT: True,
            }
        elif self.permission == PermissionTypes.FULL_ACCESS:
            return {PermissionTypes.FULL_ACCESS: True}
        raise NotImplementedError(f"invalid permission: {self.permission}")
