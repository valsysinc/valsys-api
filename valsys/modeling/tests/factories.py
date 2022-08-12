import uuid

from valsys.modeling.models import PermissionTypes, Permissions


def valid_ticker():
    return 'TIKR'


def valid_uid(rand=True):
    if rand:
        return str(uuid.uuid4())


def valid_uids(count=2):
    return [valid_uid() for _ in range(0, count)]


def valid_tags(count=2):
    return [str(uuid.uuid4()) for _ in range(count)]


def valid_permission():
    return Permissions(PermissionTypes.VIEW)


def valid_email():
    return 'you@me.com'
