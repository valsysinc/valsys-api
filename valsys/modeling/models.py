from typing import Dict


class Permissions:
    VIEW = 'view'
    EDIT = 'edit'

    @classmethod
    def get_body(cls, permission: str) -> Dict[str, bool]:
        """Generate a permissions body from the
        provided permissions string.
        
        If an invalid permission string is
        given, a `NotImplementedError` is thrown."""
        if permission == cls.VIEW:
            return {
                "view": True,
            }
        elif permission == cls.EDIT:
            return {
                "edit": True,
            }
        raise NotImplementedError(f"invalid permission: {permission}")
