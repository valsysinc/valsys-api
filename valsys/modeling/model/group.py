from dataclasses import dataclass
from typing import List


@dataclass
class Group:
    name: str
    uid: str
    user_id: str
    model_ids: List[str]

    class fields:
        UID = 'uid'
        NAME = 'name'
        USER_ID = 'userID'
        MODEL_IDS = 'modelIDs'

    @classmethod
    def from_json(cls, data):
        return cls(uid=data[cls.fields.UID],
                   name=data[cls.fields.NAME],
                   user_id=data[cls.fields.USER_ID],
                   model_ids=data[cls.fields.MODEL_IDS])
