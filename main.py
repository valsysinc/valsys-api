import datetime

from valsys.config import API_PASSWORD, API_USERNAME
from valsys.auth import authenticate
from valsys.seeds import load_company_configs, load_templates
from valsys.spawn import ModelSeedConfigurationData
from valsys.spawn import SpawnHandler
from valsys.utils import logger

auth_token = authenticate(username=API_USERNAME, password=API_PASSWORD)

configs_json = load_company_configs(count=20)[9:10]
templates = load_templates(auth_token)
template_id = templates[0].get("uid")

hist_period = 2
proj_period = 3

configs = []
for config in configs_json:
    cfg = ModelSeedConfigurationData(
        company_name=config.get("companyName"),
        ticker=config.get("ticker"),
        industry_group=config.get("industry"),
        proj_period=proj_period,
        hist_period=hist_period,
        start_period=config.get("startYears")[-1],
        start_date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        template_id=template_id,
    )

    configs.append(cfg)

tags = ["t1"]
emails = ["j@me.com"]

spawner_report = SpawnHandler.build_and_spawn_models(
    configs=configs,
    user=API_USERNAME,
    password=API_PASSWORD,
    tags=tags,
    emails=emails,
)


[logger.info(sr.jsonify(detail=True)) for sr in spawner_report]
