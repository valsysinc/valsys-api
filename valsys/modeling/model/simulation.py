from dataclasses import dataclass, field
from typing import List
from valsys.modeling.model.line_item import LineItem


@dataclass
class GroupData:
    pass


@dataclass
class ModelSimulations:
    id: str
    ticker: str
    start_period: int
    forecast_end_period: int
    historical_start_period: int
    line_items: List[LineItem] = field(default_factory=list)

    @classmethod
    def from_json(cls, data):
        return cls(id=data.get('id'),
                   ticker=data.get('ticker'),
                   start_period=data.get('startPeriod'),
                   forecast_end_period=data.get('forecastEndPeriod'),
                   historical_start_period=data.get('historicalStartPeriod'),
                   line_items=[
                       LineItem.from_json(li) for li in data.get('lineItems')
                   ])


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
