"""Driver example for spawning models"""
import datetime

from valsys.seeds.loader import SeedsLoader
from valsys.spawn.models import ModelSeedConfigurationData
from valsys.spawn.spawn_handler import SpawnHandler

loader = SeedsLoader()
configs = loader.company_configs_by_ticker(["BLIN", "BWXT"])
template_id = loader.template_id_by_name(template_name="dcf-standard")

hist_period = 2
proj_period = 3

seeds = []
for config in configs:
    seeds.append(
        ModelSeedConfigurationData(
            company_name=config.company_name,
            ticker=config.ticker,
            industry_group=config.industry,
            start_period=config.start_period,
            start_date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            proj_period=proj_period,
            hist_period=hist_period,
            template_id=template_id,
        )
    )

tags = ["t1"]
emails = ["j@me.com"]

spawner_report = SpawnHandler.build_and_spawn_models(
    seeds=seeds,
    tags=tags,
    emails=emails,
)
