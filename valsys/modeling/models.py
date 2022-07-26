from typing import Dict


class Permissions:
    VIEW = 'view'
    EDIT = 'edit'
    FULL_ACCESS = 'fullAccess'

    @classmethod
    def get_body(cls, permission: str) -> Dict[str, bool]:
        """Generate a permissions body from the
        provided permissions string.
        
        If an invalid permission string is
        given, a `NotImplementedError` is thrown."""
        if permission == cls.VIEW:
            return {
                cls.VIEW: True,
            }
        elif permission == cls.EDIT:
            return {
                cls.EDIT: True,
            }
        elif permission == cls.FULL_ACCESS:
            return {cls.FULL_ACCESS: True}
        raise NotImplementedError(f"invalid permission: {permission}")
