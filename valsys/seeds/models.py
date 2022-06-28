from dataclasses import dataclass


@dataclass
class CompanyConfig:
    company_name: str
    ticker: str
    industry: str
    start_period: float

    @classmethod
    def from_json_modeling(cls, input_json):
        return cls(
            company_name=input_json.get("companyName"),
            ticker=input_json.get("ticker"),
            industry=input_json.get("industry"),
            start_period=input_json.get("startYears")[-1],
        )
