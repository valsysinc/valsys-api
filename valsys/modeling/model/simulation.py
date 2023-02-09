from dataclasses import dataclass, field
from typing import List, Dict, Any
from valsys.modeling.model.line_item import LineItem


@dataclass
class SimpleCell:
    id: str
    identifier: str
    edges: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json(cls, data):
        return cls(id=data.get('id'),
                   identifier=data.get('identifier'),
                   edges=data.get('edges', {}))


@dataclass
class GroupField:
    field: str
    id: str
    identifier: str
    value: str
    period: float
    deps: List[SimpleCell] = field(default_factory=list)
    precs: List[SimpleCell] = field(default_factory=list)

    @classmethod
    def from_json(cls, name: str, data: Dict[str, str]):
        return cls(
            field=name,
            id=data.get('id'),
            identifier=data.get('identifier', ''),
            value=data.get('value'),
            period=data.get('period', 0),
            deps=[
                SimpleCell.from_json(dc)
                for dc in data.get('edges', {}).get('dependantCells', [])
            ],
            precs=[
                SimpleCell.from_json(dc)
                for dc in data.get('edges', {}).get('precedentCells', [])
            ])


@dataclass
class GroupModel:
    id: str
    title: str
    ticker: str
    company_name: str
    fields: List[GroupField] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        model_info = data.get('model')
        return cls(id=model_info.get('id'),
                   title=model_info.get('title'),
                   ticker=model_info.get('ticker'),
                   company_name=model_info.get('companyName'),
                   fields=[
                       GroupField.from_json(fn, fk)
                       for fn, fk in data.get('fields').items()
                   ])


@dataclass
class GroupData:
    models: List[GroupModel] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: List[Dict[str, Any]]):
        return cls(models=[GroupModel.from_json(m) for m in data])


@dataclass
class Edit:

    @classmethod
    def validate(cls, e: Dict[str, str]):
        assert 'formula' in e
        assert '$FORMULA' in e.get('formula')
        assert 'timePeriod' in e
        assert 'LFY' in e.get('timePeriod')


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
class Simulation:
    simulations: List[ModelSimulations] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: List[Dict[str, Any]]):
        return cls(simulations=[ModelSimulations.from_json(s) for s in data])


@dataclass
class SimulationResponse:
    group_data: GroupData = field(default_factory=GroupData)
    simulation: Simulation = field(default_factory=Simulation)

    class fields:
        SIMULATION = 'simulation'
        GROUP_DATA = 'groupData'

    @classmethod
    def from_json(cls, data: Dict[str, List[Dict[str, Any]]]):
        return cls(
            simulation=Simulation.from_json(data.get(cls.fields.SIMULATION)),
            group_data=GroupData.from_json(data.get(cls.fields.GROUP_DATA)))
