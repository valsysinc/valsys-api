from dataclasses import dataclass, field
from typing import List, Dict
from valsys.modeling.model.line_item import LineItem


@dataclass
class GroupData:
    pass


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
    def from_json(cls, data):
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
    def from_json(cls, data):
        return cls(simulations=[ModelSimulations.from_json(s) for s in data])


@dataclass
class SimulationResponse:
    group_data: GroupData = field(default_factory=GroupData)
    simulation: Simulation = field(default_factory=Simulation)

    @classmethod
    def from_json(cls, data):
        return cls(simulation=Simulation.from_json(data.get('simulation')))
