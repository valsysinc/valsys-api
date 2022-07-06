import json
from dataclasses import dataclass, field
from typing import Iterator, List, Tuple, Optional, Dict, Any

from tomlkit import value
from valsys.utils import logger


@dataclass
class FormulaEditConfig:
    period_name: str
    period_year: str
    formula: str

    @classmethod
    def from_json(cls, config):
        return cls(
            period_name=config.get('periodName'),
            period_year=config.get('periodYear'),
            formula=config.get('formula')
        )


@dataclass
class LineItemConfig:
    name: str
    order: str
    formula_edits: List[FormulaEditConfig] = field(default_factory=list)

    @classmethod
    def from_json(cls, config):
        return cls(name=config.get('name'), order=config.get('order'),
                   formula_edits=[FormulaEditConfig.from_json(fec) for fec in config.get('formulaEdits')])


@dataclass
class PopulateModulesConfig:
    model_ids: List[str]
    parent_module_name: str
    module_name: str
    key_metrics_config: Dict[str, Any]
    line_item_data: List[LineItemConfig] = field(default_factory=list)

    def validate(self):
        if self.parent_module_name == "":
            raise ValueError(f"need parentModuleName")
        if self.module_name == "":
            raise ValueError(f"need moduleName")

    def get_line_item_config(self, line_item_name: str) -> LineItemConfig:
        for li in self.line_item_data:
            if li.name == line_item_name:
                return li
        raise ValueError(f"line item with name {line_item_name} not found in config")

    def __post__init__(self):
        self.validate()

    @classmethod
    def from_json(cls, model_ids: List[str], config: Dict[str, Any]):
        return cls(
            model_ids=model_ids,
            parent_module_name=config.get('parentModuleName', ''),
            module_name=config.get('moduleName', ''),
            key_metrics_config=config.get('keyMetricsConfig'),
            line_item_data=[LineItemConfig.from_json(li) for li in config.get('lineItems')]
        )


@dataclass
class ModelSpawnConfig:
    tickers: List[str]
    template_name: str
    hist_period: int
    proj_period: int
    tags: List[str] = field(default_factory=list)
    emails: List[str] = field(default_factory=list)

    def validate(self):
        if len(self.tickers) == 0:
            raise ValueError('need tickers')
        if self.template_name == "":
            raise ValueError('need a templateName')
        if self.hist_period is None:
            raise ValueError('need histPeriod')
        if self.proj_period is None:
            raise ValueError('need projPeriod')

    def __post__init__(self):
        self.validate()

    @classmethod
    def from_json(cls, spawn_config):
        return cls(
            tickers=spawn_config.get('tickers'),
            template_name=spawn_config.get('templateName'),
            hist_period=spawn_config.get('histPeriod', None),
            proj_period=spawn_config.get('projPeriod', None),
            tags=spawn_config.get('tags', []),
            emails=spawn_config.get('emails', []),
        )

    def jsonify(self):
        return {
            'tickers': self.tickers,
            'templateName': self.templateName,
            'histPeriod': self.hist_period,
            'projPeriod': self.projPeriod,
            'tags': self.tags,
            'emails': self.emails
        }


@dataclass
class ModelSeedConfigurationData:
    """ModelSeedConfigurationData is the required data structure
    for spawning models."""

    company_name: str
    ticker: str
    template_id: str
    proj_period: int
    hist_period: int
    industry_group: str
    start_period: int
    start_date: str
    action: str = ""
    model_type: str = "DEFAULT"
    period_type: str = "ANNUAL"
    cash_flow_type: str = "FCFF"
    valuation_type: str = "Perpetual Growth"
    company_type: str = "Public"
    target_variable: str = "Implied share price"

    @property
    def hist_max(self):
        """Compute the historical max."""
        return self.start_period - self.hist_period + 1

    @property
    def hist_min(self):
        """Compute the historical min."""
        return self.start_period + self.proj_period

    def jsonify(self):
        return {
            "action": self.action,
            "companyName": self.company_name,
            "ticker": self.ticker,
            "templateID": self.template_id,
            "numForecastYears": self.proj_period,
            "numHistoricalYears": self.hist_period,
            "industry": self.industry_group,
            "startPeriod": self.start_period,
            "startDate": self.start_date,
            "type": self.model_type,
            "periodType": self.period_type,
            "cashFlowType": self.cash_flow_type,
            "valuationType": self.valuation_type,
            "companyType": self.company_type,
            "targetVariable": self.target_variable,
            "historicalMax": self.hist_max,
            "historicalMin": self.hist_min,
        }

    def validate(self):
        nexpected_fields = 17
        assert len(self.jsonify()) == nexpected_fields


@dataclass
class SpawnProgress:
    model_id: str = ""
    ticker: str = ""
    spawned: bool = False
    tagged: bool = False
    shared: bool = False
    spawn_error: Exception = None
    tag_error: Exception = None
    share_error: Exception = None
    shared_to: List[Tuple[str,
                          Optional[Exception]]] = field(default_factory=list)

    @property
    def all_complete(self):
        return self.spawned and self.tagged and self.shared

    def mark_tagged(self, err=None):
        if err is None:
            self.tagged = True
        self.tag_error = err

    def mark_shared(self, email: str, permission: str, err=None):
        if err is None:
            self.shared = True
        self.shared_to.append((email, permission, err))

    def mark_spawned(self, model_id: str = None, err=None):
        if err is None:
            self.spawned = True
            self.model_id = model_id
        else:
            self.spawn_error = err

    def jsonify(self, detail=False):
        """Returns a json representation of the progress;

        If `detail=True`, then any error messages are returned as well.

        `detail=False` by default.
        """
        j = {
            "modelID": self.model_id,
            "ticker": self.ticker,
            "spawned": self.spawned,
            "tagged": self.tagged,
            "shared": self.shared,
        }
        if detail:
            j.update({
                "spawnError":
                str(self.spawn_error or ""),
                "tagError":
                str(self.tag_error or ""),
                "sharedTo": [{
                    "email": e,
                    "permission": p,
                    "error": str(err or "")
                } for e, p, err in self.shared_to],
            })
        return j


@dataclass
class SpawnerProgress:
    options: Dict[str, Any] = field(default_factory=dict)
    processes: List[SpawnProgress] = field(default_factory=list)
    verbose: bool = False

    def __post_init__(self):
        self.verbose = self.options.get("verbose", False)

    def append(self, process: SpawnProgress):
        self.processes.append(process)
        if self.verbose:
            logger.info(process.jsonify(detail=True))

    def __iter__(self) -> Iterator[SpawnProgress]:
        for p in self.processes:
            yield p

    @property
    def spawned_model_ids(self):
        return [p.model_id for p in self if p.spawned]

    @property
    def has_errors(self):
        return len(self.spawned_model_ids) == 0
