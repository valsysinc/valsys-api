from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

from valsys.modeling.model.line_item import LineItem


@dataclass
class SimpleCell:
    id: str
    identifier: str
    edges: Dict[str, Any] = field(default_factory=dict)

    class fields:
        ID = 'id'
        IDENTIFIER = 'identifier'
        EDGES = 'edges'

    @classmethod
    def from_json(cls, data):
        return cls(id=data.get(cls.fields.ID),
                   identifier=data.get(cls.fields.IDENTIFIER),
                   edges=data.get(cls.fields.EDGES, {}))


@dataclass
class GroupField:
    field: str
    id: str
    identifier: str
    value: str
    period: float
    deps: List[SimpleCell] = field(default_factory=list)
    precs: List[SimpleCell] = field(default_factory=list)

    class fields:
        ID = 'id'
        IDENTIFIER = 'identifier'
        VALUE = 'value'
        PERIOD = 'period'
        EDGES = 'edges'
        DEP_CELLS = 'dependantCells'
        PRE_CELLS = 'precedentCells'

    @classmethod
    def from_json(cls, name: str, data: Dict[str, str]):
        return cls(field=name,
                   id=data.get(cls.fields.ID),
                   identifier=data.get(cls.fields.IDENTIFIER, ''),
                   value=data.get(cls.fields.VALUE),
                   period=data.get(cls.fields.PERIOD, 0),
                   deps=[
                       SimpleCell.from_json(dc) for dc in data.get(
                           cls.fields.EDGES, {}).get(cls.fields.DEP_CELLS, [])
                   ],
                   precs=[
                       SimpleCell.from_json(dc) for dc in data.get(
                           cls.fields.EDGES, {}).get(cls.fields.PRE_CELLS, [])
                   ])


@dataclass
class GroupModel:
    id: str
    title: str
    ticker: str
    company_name: str
    group_fields: List[GroupField] = field(default_factory=list)

    class fields:
        MODEL = 'model'
        ID = 'id'
        TITLE = 'title'
        TICKER = 'ticker'
        COMPANY_NAME = 'companyName'
        FIELDS = 'fields'

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        model_info = data.get(cls.fields.MODEL)
        return cls(id=model_info.get(cls.fields.ID),
                   title=model_info.get(cls.fields.TITLE),
                   ticker=model_info.get(cls.fields.TICKER),
                   company_name=model_info.get(cls.fields.COMPANY_NAME),
                   group_fields=[
                       GroupField.from_json(fn, fk)
                       for fn, fk in data.get(cls.fields.FIELDS).items()
                   ])


@dataclass
class Edit:

    @classmethod
    def validate(cls, e: Dict[str, str]):
        required_keys = ['formula', 'timePeriod']
        for k in required_keys:
            assert k in e.keys()
        assert '$FORMULA' in e.get('formula')
        assert 'LFY' in e.get('timePeriod')
        return True


@dataclass
class ModelSimulations:
    id: str
    ticker: str
    start_period: int
    forecast_end_period: int
    historical_start_period: int
    line_items: List[LineItem] = field(default_factory=list)

    class fields:
        ID = 'id'
        TICKER = 'ticker'
        START_PERIOD = 'startPeriod'
        FORECAST_END_PERIOD = 'forecastEndPeriod'
        HISTORICAL_START_PERIOD = 'historicalStartPeriod'
        LINE_ITEMS = 'lineItems'

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        return cls(id=data.get(cls.fields.ID),
                   ticker=data.get(cls.fields.TICKER),
                   start_period=data.get(cls.fields.START_PERIOD),
                   forecast_end_period=data.get(
                       cls.fields.FORECAST_END_PERIOD),
                   historical_start_period=data.get(
                       cls.fields.HISTORICAL_START_PERIOD),
                   line_items=[
                       LineItem.from_json(li)
                       for li in data.get(cls.fields.LINE_ITEMS)
                   ])

    @classmethod
    def validate_edits(cls, es: List[Dict[str, str]]):
        [Edit.validate(e) for e in es]
        return


@dataclass
class SimulationResponse:
    group_data: List[GroupModel] = field(default_factory=list)
    simulation: List[ModelSimulations] = field(default_factory=list)

    class fields:
        SIMULATION = 'simulation'
        GROUP_DATA = 'groupData'

    @classmethod
    def from_json(cls, data: Dict[str, List[Dict[str, Any]]]):
        return cls(simulation=[
            ModelSimulations.from_json(s)
            for s in data.get(cls.fields.SIMULATION)
        ],
                   group_data=[
                       GroupModel.from_json(g)
                       for g in data.get(cls.fields.GROUP_DATA)
                   ])

    @property
    def group_fields(self) -> Set[str]:
        flds = set()
        for f in self.group_data:
            for n in f.group_fields:
                flds.add(n.field)
        return flds
