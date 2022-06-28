from typing import List
from .service import load_company_configs
from .service import load_templates
from .models import CompanyConfig


class SeedsLoader:
    """SeedsLoader is responsible for loading configs
    and IDs for use in the Spawner."""

    def company_configs_by_ticker(self, tickers: List[str]) -> List[CompanyConfig]:
        """Load a list of company configs by ticker from
        the valsys modeling service API."""

        ret = []
        for cfg in load_company_configs():
            if cfg.get("ticker") in tickers:
                ret.append(CompanyConfig.from_json_modeling(cfg))
        return ret

    def template_id_by_name(self, template_name: str) -> str:
        """Load the template ID by the template name.

        Raises a ValueError if the template cannot be found."""

        for template in load_templates():
            if template.get("template_name") == template_name:
                return template.get("uid")
        raise ValueError(f"template not found for template_name: {template_name}")
