from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CompanyConfig:
    """CompanyConfig is the required data structure for
    producing model seeds.

    Can add custom class methods for alternative data sources."""

    company_name: str
    ticker: str
    industry: str
    start_period: float

    @classmethod
    def from_json_modeling(cls, input_json: Dict[str, Any]):
        return cls(
            company_name=input_json.get("companyName"),
            ticker=input_json.get("ticker"),
            industry=input_json.get("industry"),
            start_period=input_json.get("startYears")[-1],
        )


@dataclass
class OrchestratorModelConfig:
    ticker: str
    company_name: str
    industry: str
    geography: str
    currency: str
    start_period: int
    title: str = ''

    def jsonify(self):
        return {
            "title": self.title,
            "ticker": self.ticker,
            "companyName": self.company_name,
            "industry": self.industry,
            "geography": self.geography,
            "currency": self.currency,
            "startPeriod": self.start_period
        }


@dataclass
class OrchestratorConfig:

    username: str
    password: str
    template_id: str
    period_type: str
    start_date: str
    num_forecast_years: int
    num_historical_years: int
    model_configs: List[OrchestratorModelConfig] = field(default_factory=list)
    action: str = ''

    def jsonify(self):
        return {
            "action": "SPAWN_MODELS",
            "username": self.username,
            "password": self.password,
            "templateID": self.template_id,
            "periodType": self.period_type,
            "startDate": self.start_date,
            "numForecastYears": self.num_forecast_years,
            "numHistoricalYears": self.num_historical_years,
            "modelConfigs": [omc.jsonify() for omc in self.model_configs]
        }
