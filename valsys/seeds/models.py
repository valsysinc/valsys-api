from dataclasses import dataclass, field
from typing import Any, Dict, List
import datetime

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


@dataclass
class CompanyConfig:
    """CompanyConfig is the required data structure for
    producing model seeds.

    Can add custom class methods for alternative data sources."""

    company_name: str
    ticker: str
    industry: str
    start_period: float
    geography: str
    currency: str

    @classmethod
    def from_json_modeling(cls, input_json: Dict[str, Any]):
        return cls(company_name=input_json.get("companyName"),
                   ticker=input_json.get("ticker"),
                   industry=input_json.get("industry"),
                   start_period=input_json.get("startYears")[-1],
                   geography=input_json.get('geography'),
                   currency=input_json.get('currency'))


@dataclass
class OrchestratorModelConfig:
    ticker: str
    company_name: str = ''
    industry: str = ''
    geography: str = ''
    currency: str = 'USD'
    start_period: int = 0
    title: str = ''
    template_id: str = ''

    def update(self, company_info: CompanyConfig):
        self.company_name = company_info.company_name
        self.industry = company_info.industry
        self.geography = company_info.geography
        self.start_period = company_info.start_period

    def jsonify(self):
        return {
            "title": self.title,
            "ticker": self.ticker,
            "companyName": self.company_name,
            "industry": self.industry,
            "geography": self.geography,
            "currency": self.currency,
            "startPeriod": self.start_period,
            "templateID": self.template_id,
        }


@dataclass
class OrchestratorConfig:

    num_forecast_years: int
    num_historical_years: int
    start_date: str = datetime.datetime.now().strftime(DATETIME_FORMAT)

    username: str = ''
    password: str = ''
    period_type: str = "ANNUAL"
    model_configs: List[OrchestratorModelConfig] = field(default_factory=list)

    action: str = ''
    template_name: str = ''

    tags: List[str] = field(default_factory=list)
    emails: List[str] = field(default_factory=list)

    @property
    def tickers(self):
        return [mc.ticker for mc in self.model_configs]

    @property
    def count_tickers(self):
        return len(self.model_configs)

    def jsonify(self):
        return {
            "action": self.action,
            "username": self.username,
            "password": self.password,
            "periodType": self.period_type,
            "startDate": self.start_date,
            "numForecastYears": self.num_forecast_years,
            "numHistoricalYears": self.num_historical_years,
            "modelConfigs": [omc.jsonify() for omc in self.model_configs]
        }

    @classmethod
    def from_json(cls, ij):
        return cls(template_name=ij.get('templateName'),
                   num_forecast_years=ij.get('numForecastYears'),
                   num_historical_years=ij.get('numHistoricalYears'),
                   period_type=ij.get('periodType', 'ANNUAL'),
                   tags=ij.get('tags', []),
                   start_date=ij.get(
                       'startDate',
                       datetime.datetime.now().strftime(DATETIME_FORMAT)),
                   emails=ij.get('emails', []),
                   model_configs=[
                       OrchestratorModelConfig(t) for t in ij.get('tickers')
                   ])
