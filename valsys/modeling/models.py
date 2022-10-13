from dataclasses import dataclass, field
from typing import Dict, List

from valsys.modeling.exceptions import FilterModelsException


@dataclass
class SpawnedModelInfo:
    model_id: str
    ticker: str

    @classmethod
    def from_json(cls, m):
        return cls(model_id=m.get('id'), ticker=m.get('ticker'))


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


@dataclass
class PermissionsModel:
    user_id: str
    model_id: str
    view: bool = False
    edit: bool = False
    full_access: bool = False
    owner: bool = False

    class fields:
        USER_ID = 'userID'
        MODEL_ID = 'modelID'
        VIEW = 'view'
        EDIT = 'edit'
        FULL_ACCESS = 'fullAccess'
        OWNER = 'owner'

    def jsonify(self):
        return {
            self.fields.USER_ID: self.user_id,
            self.fields.MODEL_ID: self.model_id,
            self.fields.VIEW: self.view,
            self.fields.EDIT: self.edit,
            self.fields.FULL_ACCESS: self.full_access,
            self.fields.OWNER: self.owner
        }

    @classmethod
    def from_json(cls, j):
        return cls(user_id=j.get(cls.fields.USER_ID),
                   model_id=j.get(cls.fields.MODEL_ID),
                   view=j.get(cls.fields.VIEW, False),
                   edit=j.get(cls.fields.EDIT, False),
                   full_access=j.get(cls.fields.FULL_ACCESS, False),
                   owner=j.get(cls.fields.OWNER, False))


@dataclass
class ModelDetailInformation:
    uid: str
    cik: str
    ticker: str
    company_name: str
    geography: str
    industry: str
    currency: str
    case_id: str
    current_share_price: float
    implied_share_price: float
    forecast_period: int
    historical_period: int
    historical_start: int
    forecast_increment: int
    start_period: int
    created_at: str
    last_edit: str
    tags: List[str]
    model_tags: List[str]
    permissions: PermissionsModel

    @classmethod
    def from_json(cls, j):
        return cls(uid=j.get('uid'),
                   cik=j.get('cik'),
                   ticker=j.get('ticker'),
                   geography=j.get('geography'),
                   industry=j.get('industry'),
                   company_name=j.get('companyName'),
                   currency=j.get('currency'),
                   case_id=j.get('caseID'),
                   current_share_price=float(j.get('currentSharePrice')),
                   implied_share_price=float(j.get('impliedSharePrice')),
                   forecast_period=int(j.get('forecastPeriod')),
                   historical_period=int(j.get('historicalPeriod')),
                   historical_start=int(j.get('historicalStart')),
                   forecast_increment=j.get('forecastIncrement'),
                   start_period=j.get('startPeriod'),
                   created_at=j.get('createdAt'),
                   last_edit=j.get('lastEdit'),
                   tags=j.get('tags'),
                   model_tags=j.get('modelTags'),
                   permissions=PermissionsModel.from_json(
                       j.get('permissions')))


@dataclass
class ModelsFilter:
    max_date: str
    min_date: str

    predicate: str
    model_type: str
    filter_name: bool = False
    filter_ticker: bool = False
    filter_geography: bool = False
    filter_industry: bool = False
    geo_filters: List[str] = field(default_factory=list)
    ind_filters: List[str] = field(default_factory=list)
    tag_filters: List[str] = field(default_factory=list)
    tag_filter_type: str = ''

    class ValidTypes:
        TAG_FILTER_TYPES = ['', 'and', 'or']
        MODEL_TYPES = ['user', 'shared', 'both']

    def __post_init__(self):
        self.validate()

    def set_filter_on(self, filter_on: List[str]):
        if filter_on is None:
            return
        filter_on = [fo.lower() for fo in filter_on]
        self.filter_name = 'name' in filter_on
        self.filter_ticker = 'ticker' in filter_on
        self.filter_geography = 'geography' in filter_on
        self.filter_industry = 'industry' in filter_on

    def validate(self):
        if self.tag_filter_type not in self.ValidTypes.TAG_FILTER_TYPES:
            raise FilterModelsException(
                f"invalid tag_filter_type prop: {self.tag_filter_type}")

        if self.model_type not in self.ValidTypes.MODEL_TYPES:
            raise FilterModelsException(
                f"invalid model_type prop: {self.model_type}")

    def jsonify(self):
        # Incase anyone has messed about with anything: validate again;
        self.validate()
        return {
            "maxDate": self.max_date,
            "minDate": self.min_date,
            "filters": {
                "Name": self.filter_name,
                "Ticker": self.filter_ticker,
                "Geography": self.filter_geography,
                "Industry": self.filter_industry
            },
            "geoFilters": self.geo_filters,
            "indFilters": self.ind_filters,
            "tagFilters": self.tag_filters,
            "tagFilterType": self.tag_filter_type,
            "predicate": self.predicate,
            "modelType": self.model_type,
        }
