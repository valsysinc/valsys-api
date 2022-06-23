import datetime
from dataclasses import dataclass, field
from typing import List, Any, Dict


@dataclass
class ModelSeedConfigurationData:
    company_name: str
    ticker: str
    template_id: str
    proj_period: int
    hist_period: int
    industry_group: str
    start_period: int
    start_date: str
    data_source: str
    model_type: str = "DEFAULT"
    period_type: str = "ANNUAL"
    cash_flow_type: str = "FCFF"
    valuation_type: str = "Perpetual Growth"
    company_type: str = "Public"
    target_variable: str = "Implied share price"

    @classmethod
    def from_row(cls, row, proj_period, hist_period):
        return cls(
            company_name=row.companyName,
            ticker=row.ticker,
            template_id=row.template_id,
            industry_group=row.IndustryGroup,
            start_period=row.fiscalYear,
            start_date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            data_source=row.source,
            proj_period=proj_period,
            hist_period=hist_period,
        )

    @classmethod
    def from_api(cls, ij, proj_period, hist_period):
        ys = ij.get("startYears")
        ys.reverse()
        return cls(
            company_name=ij.get("companyName"),
            ticker=ij.get("ticker"),
            template_id=ij.get("templateID"),
            industry_group=ij.get("industry"),
            proj_period=proj_period,
            hist_period=hist_period,
            start_period=ys[0],
            start_date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            data_source="",
        )

    def jsonify(self):
        return {
            "action": "CREATE_MODEL",
        }
        return {
            "action": "CREATE_MODEL",
            "companyName": self.company_name,
            "ticker": self.ticker,
            "templateID": self.template_id,
            "projectionPeriod": self.proj_period,
            "historicalPeriod": self.hist_period,
            "industry": self.industry_group,
            "startPeriod": self.start_period,
            "startDate": self.start_date,
            "type": self.model_type,
            "periodType": self.period_type,
            "cashFlowType": self.cash_flow_type,
            "valuationType": self.valuation_type,
            "companyType": self.company_type,
            "targetVariable": self.target_variable,
            "variables": {"INTERNAL_SOURCE": self.data_source},
            "historicalMax": self.start_period - self.hist_period + 1,
            "historicalMin": self.start_period + self.proj_period,
        }

    def pp(self):
        print("params:")
        [print(f"{k}={v}") for k, v in self.jsonify().items()]


@dataclass
class SpawnerError:
    name: str
    exception: Exception = None
    info: Dict[str, Any] = field(default_factory=dict)

    def jsonify(self):
        return {
            "name": self.name,
            "info": self.info,
            "exception_msg": str(self.exception),
        }


@dataclass
class SpawnerErrors:
    errors: List[SpawnerError] = field(default_factory=SpawnerError)

    def append(self, error: SpawnerError):
        self.errors.append(error)

    def jsonify(self):
        return [e.jsonify() for e in self.errors]

    def __len__(self):
        return len(self.errors)


@dataclass
class SpawnerReport:
    configs: List[Dict[str, Any]] = field(default_factory=dict)
    errors: SpawnerErrors = field(default_factory=SpawnerErrors)

    @property
    def has_errors(self):
        return len(self.errors) > 0
