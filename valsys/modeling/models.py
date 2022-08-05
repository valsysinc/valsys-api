from dataclasses import dataclass, field
from typing import Dict, List


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


@dataclass
class ModelGroup:
    uid: str
    name: str
    user_id: str
    model_ids: List[str] = field(default_factory=list)

    def jsonify(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'userID': self.user_id,
            'modelIDs': self.model_ids
        }

    @classmethod
    def from_json(cls, ij):
        return cls(uid=ij.get('uid'),
                   name=ij.get('name'),
                   user_id=ij.get('userID'),
                   model_ids=ij.get('modelIDs'))


@dataclass
class ModelGroups:
    groups: List[ModelGroup] = field(default_factory=list)

    def __iter__(self):
        for g in self.groups:
            yield g

    def jsonify(self):
        return {'groups': [g.jsonify() for g in self.groups]}

    @classmethod
    def from_json(cls, ij):
        mg = cls()
        [mg.groups.append(ModelGroup.from_json(mj)) for mj in ij]
        return mg


@dataclass
class TaggedLineItemResponse:
    uid: str
    name: str
    tags: List[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, j):
        return cls(uid=j.get('uid'), name=j.get('name'), tags=j.get('tags'))
