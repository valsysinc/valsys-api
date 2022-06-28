"""Driver example for spawning models"""
import datetime

from valsys.seeds.loader import SeedsLoader
from valsys.spawn.models import ModelSeedConfigurationData
from valsys.spawn.spawn_handler import SpawnHandler

loader = SeedsLoader()
configs_json = loader.company_configs_by_ticker(["BLIN", "BWXT"])
template_id = loader.template_id_by_name(template_name="dcf-standard")

hist_period = 2
proj_period = 3

configs = []
for config in configs_json:
    configs.append(
        ModelSeedConfigurationData(
            company_name=config.get("companyName"),
            ticker=config.get("ticker"),
            industry_group=config.get("industry"),
            start_period=config.get("startYears")[-1],
            start_date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            proj_period=proj_period,
            hist_period=hist_period,
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
