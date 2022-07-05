from typing import Dict, Any
import datetime
from valsys.utils import logger
from valsys.seeds.loader import SeedsLoader
from valsys.spawn.models import ModelSeedConfigurationData
from valsys.spawn.spawn_handler import SpawnHandler


def spawn(config: Dict[str, Any]):

    tickers = config.get('tickers')
    template_name = config.get('template_name')
    proj_period = config.get('proj_period')
    hist_period = config.get('hist_period')
    tags = config.get('tags')
    emails = config.get('emails')

    logger.info(f"running spawn with {config}")

    loader = SeedsLoader()
    configs = loader.company_configs_by_ticker(tickers)
    template_id = loader.template_id_by_name(template_name=template_name)

    seeds = []
    for config in configs:
        seeds.append(
            ModelSeedConfigurationData(
                company_name=config.company_name,
                ticker=config.ticker,
                industry_group=config.industry,
                start_period=config.start_period,
                start_date=datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"),
                proj_period=proj_period,
                hist_period=hist_period,
                template_id=template_id,
            ))

    return SpawnHandler.build_and_spawn_models(
        seeds=seeds,
        tags=tags,
        emails=emails,
    )