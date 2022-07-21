from dataclasses import dataclass
from typing import Any, Dict


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
