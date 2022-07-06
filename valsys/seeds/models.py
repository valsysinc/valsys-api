from typing import Dict, Any
from dataclasses import dataclass


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
