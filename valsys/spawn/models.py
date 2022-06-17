import datetime
from dataclasses import dataclass


@dataclass
class SeedDataFrameRow:
    companyName: str
    ticker: str
    template_id: str
    IndustryGroup: str
    fiscalYear: int
    source: str


@dataclass
class ModelSeedConfigurationData:
    company_name: str
    ticker: str
    template_id: str
    proj_period: int
    hist_period: int
    industry_group: str
    fiscal_year: int
    start_period: int
    start_date: str
    data_source: str
    model_type: str = "DEFAULT"
    period_type: str = 'ANNUAL'
    cash_flow_type: str = 'FCFF'
    valuation_type: str = 'Perpetual Growth'
    company_type: str = 'Public'
    target_variable: str = 'Implied share price'

    @classmethod
    def from_row(cls, row: SeedDataFrameRow, proj_period, hist_period):
        return cls(
            company_name=row.companyName,
            ticker=row.ticker,
            template_id=row.template_id,
            industry=row.IndustryGroup,
            start_period=row.fiscalYear,
            start_date=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            data_source=row.source,
            proj_period=proj_period, hist_period=hist_period
        )

    def jsonify(self):
        return {
            "companyName": self.companyName,
            "ticker": self.ticker,
            "templateID": self.template_id,
            "projectionPeriod": self.proj_period,
            "historicalPeriod": self.hist_period,
            "industry": self.IndustryGroup,
            "startPeriod": self.fiscalYear,
            "startDate": self.start_date,
            "type": self.model_type,
            "periodType": self.period_type,
            "cashFlowType": self.cash_flow_type,
            "valuationType": self.valuation_type,
            "companyType": self.company_type,
            "targetVariable": self.target_variable,
            "variables": {
                "INTERNAL_SOURCE": self.data_source
            },
            "historicalMax": self.fiscalYear - self.hist_period + 1,
            "historicalMin": self.fiscalYear + self.proj_period
        }
