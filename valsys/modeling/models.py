from dataclasses import dataclass, field
from typing import Any, Dict, List

from valsys.modeling.exceptions import (
    FilterModelsException,
    SpawnModelResponseException,
)


@dataclass
class SpawnedModelInfo:
    model_id: str
    ticker: str

    class fields:
        MODEL_ID = 'modelID'
        TICKER = 'ticker'

    @classmethod
    def from_json(cls, m):
        mid = m.get(cls.fields.MODEL_ID, None)
        if mid is None:
            raise SpawnModelResponseException("no modelID in response")
        if mid == "":
            raise SpawnModelResponseException("no modelID in response")

        return cls(model_id=mid, ticker=m.get(cls.fields.TICKER))


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

    class fields:
        UID = 'uid'
        NAME = 'name'
        USER_ID = 'userID'
        MODEL_IDS = 'modelIDs'

    def jsonify(self):
        return {
            self.fields.UID: self.uid,
            self.fields.NAME: self.name,
            self.fields.USER_ID: self.user_id,
            self.fields.MODEL_IDS: self.model_ids
        }

    @classmethod
    def from_json(cls, ij):
        return cls(uid=ij.get(cls.fields.UID),
                   name=ij.get(cls.fields.NAME),
                   user_id=ij.get(cls.fields.USER_ID),
                   model_ids=ij.get(cls.fields.MODEL_IDS))


@dataclass
class ModelGroups:
    groups: List[ModelGroup] = field(default_factory=list)

    class fields:
        GROUPS = 'groups'

    def __iter__(self):
        for g in self.groups:
            yield g

    def jsonify(self):
        return {self.fields.GROUPS: [g.jsonify() for g in self.groups]}

    def append(self, group: ModelGroup):
        self.groups.append(group)

    @classmethod
    def from_json(cls, ij: List[Dict[str, Any]]):
        mg = cls()
        if ij is None:
            return mg
        [mg.append(ModelGroup.from_json(mj)) for mj in ij]
        return mg


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

    class fields:
        ID = 'id'
        CIK = 'cik'
        TICKER = 'ticker'
        GEOGRAPHY = 'geography'
        INDUSTRY = 'industry'
        COMPANY_NAME = 'companyName'
        CURRENCY = 'currency'
        CASE_ID = 'caseID'
        CURR_SHARE_PRICE = 'currentSharePrice'
        IMPL_SHARE_PRICE = 'impliedSharePrice'
        FORE_PERIOD = 'forecastPeriod'
        HIST_PERIOD = 'historicalPeriod'
        HIST_START = 'historicalStart'
        FORE_INC = 'forecastIncrement'
        START_PERIOD = 'startPeriod'
        CREATED_AT = 'createdAt'
        LAST_EDIT = 'lastEdit'
        TAGS = 'tags'
        MODEL_TAGS = 'modelTags'
        PERMISSIONS = 'permissions'

    @classmethod
    def from_json(cls, j):
        return cls(
            uid=j.get(cls.fields.ID),
            cik=j.get(cls.fields.CIK),
            ticker=j.get(cls.fields.TICKER),
            geography=j.get(cls.fields.GEOGRAPHY),
            industry=j.get(cls.fields.INDUSTRY),
            company_name=j.get(cls.fields.COMPANY_NAME),
            currency=j.get(cls.fields.CURRENCY),
            case_id=j.get(cls.fields.CASE_ID),
            current_share_price=float(j.get(cls.fields.CURR_SHARE_PRICE, 0)),
            implied_share_price=float(j.get(cls.fields.IMPL_SHARE_PRICE, 0)),
            forecast_period=int(j.get(cls.fields.FORE_PERIOD)),
            historical_period=int(j.get(cls.fields.HIST_PERIOD)),
            historical_start=int(j.get(cls.fields.HIST_START, 0)),
            forecast_increment=j.get(cls.fields.FORE_INC),
            start_period=j.get(cls.fields.START_PERIOD),
            created_at=j.get(cls.fields.CREATED_AT),
            last_edit=j.get(cls.fields.LAST_EDIT),
            tags=j.get(cls.fields.TAGS),
            model_tags=j.get(cls.fields.MODEL_TAGS),
            permissions=PermissionsModel.from_json(
                j.get(cls.fields.PERMISSIONS)))


@dataclass
class ModelDetailInformationWithFields:
    model: ModelDetailInformation
    fields: Dict[str, str] = field(default_factory=dict)

    @property
    def uid(self):
        return self.model.uid

    @property
    def ticker(self):
        return self.model.ticker

    @classmethod
    def from_json(cls, j):
        if 'model' in j:
            model_json = j.get('model')
        else:
            model_json = j

        return cls(model=ModelDetailInformation.from_json(model_json),
                   fields=j.get('fields', {}))


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
    fields: List[str] = field(default_factory=list)

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

    def add_fields(self, fields):
        for f in fields:
            self.fields.append(f)

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
        j = {
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
            'fields': self.fields
        }

        return j
