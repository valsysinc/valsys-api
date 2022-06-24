import datetime

from valsys.config import API_PASSWORD, API_USERNAME

from valsys.seeds import (
    load_template_id_by_name,
    load_company_configs_by_ticker,
)
from valsys.spawn import ModelSeedConfigurationData
from valsys.spawn import SpawnHandler
from valsys.utils import logger


configs_json = load_company_configs_by_ticker(["BLIN", "BWXT"])
template_id = load_template_id_by_name(template_name="dcf-standard")

hist_period = 2
proj_period = 3

configs = []
for config in configs_json:
    configs.append(
        ModelSeedConfigurationData(
            company_name=config.get("companyName"),
            ticker=config.get("ticker"),
            industry_group=config.get("industry"),
            proj_period=proj_period,
            hist_period=hist_period,
            start_period=config.get("startYears")[-1],
            start_date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            template_id=template_id,
        )
    )

tags = ["t1"]
emails = ["j@me.com"]

spawner_report = SpawnHandler.build_and_spawn_models(
    configs=configs,
    tags=tags,
    emails=emails,
)

[logger.info(sr.jsonify(detail=True)) for sr in spawner_report]
