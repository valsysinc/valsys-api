import uuid

from valsys.modeling.models import PermissionTypes, Permissions
from valsys.modeling.models import ModelsFilter


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


def valid_name():
    return 'gkrhgkherjkeh'


def valid_models_filter():
    max_date = '1234'
    min_date = '4567'
    predicate = 'hello'
    model_type = ModelsFilter.ValidTypes.MODEL_TYPES[0]
    tag_filter_type = ModelsFilter.ValidTypes.TAG_FILTER_TYPES[0]
    return ModelsFilter(max_date=max_date,
                        min_date=min_date,
                        predicate=predicate,
                        model_type=model_type,
                        tag_filter_type=tag_filter_type)
