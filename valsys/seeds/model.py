import datetime
from dataclasses import dataclass

from valsys.seeds.loader import SeedsLoader
from valsys.spawn.models import ModelSpawnConfig


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


@dataclass
class ModelSeedConfigurationData:
    """ModelSeedConfigurationData is the required data structure
    for spawning models."""

    company_name: str
    ticker: str
    proj_period: int
    hist_period: int
    industry_group: str
    start_period: int
    start_date: str
    action: str = ""
    template_id: str = ''
    template_name: str = ''
    model_type: str = "DEFAULT"
    period_type: str = "ANNUAL"
    cash_flow_type: str = "FCFF"
    valuation_type: str = "Perpetual Growth"
    company_type: str = "Public"
    target_variable: str = "Implied share price"

    def __post_init__(self):
        if self.template_name != "" and self.template_id == '':
            self.template_id = SeedsLoader.template_id_by_name(
                template_name=self.template_name)
        if self.template_id == '':
            raise ValueError('need template_id')

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

    @classmethod
    def from_model_spawn_config(cls, config: ModelSpawnConfig,
                                proj_period: int, hist_period: int,
                                template_id: str):
        return cls(
            company_name=config.company_name,
            ticker=config.ticker,
            industry_group=config.industry,
            start_period=config.start_period,
            start_date=datetime.datetime.now().strftime(DATETIME_FORMAT),
            proj_period=proj_period,
            hist_period=hist_period,
            template_id=template_id,
        )
