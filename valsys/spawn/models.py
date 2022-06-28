from dataclasses import dataclass, field
from typing import Iterable, List, Tuple, Optional, Dict, Any
from valsys.utils import logger


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
    shared_to: List[Tuple[str, Optional[Exception]]] = field(default_factory=list)

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
            j.update(
                {
                    "spawnError": str(self.spawn_error or ""),
                    "tagError": str(self.tag_error or ""),
                    "sharedTo": [
                        {"email": e, "permission": p, "error": str(err or "")}
                        for e, p, err in self.shared_to
                    ],
                }
            )
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
            logger.info(process.jsonify())

    def __iter__(self) -> Iterable[SpawnProgress]:
        for p in self.processes:
            yield p
