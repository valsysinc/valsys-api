from typing import List, Dict

from valsys.seeds.loader import SeedsLoader
from valsys.seeds.models import OrchestratorConfig, OrchestratorModelConfig
from valsys.utils import loggerIT as logger


def gen_cell_identifier(config):
    return f"[{config['startingModule']}[{config['targetLineItem']}[{config['targetCellPeriod']}]]]"


def gen_orch_config(cfg: Dict[str, str], user: str, password: str):
    """Generate an orchestrator config.

    If the `templateId` is given, use that, else use the `templateName`.

    """

    template_id = cfg.get('templateId', None)
    if template_id is None:
        template_id = SeedsLoader.template_id_by_name(cfg.get('templateName'))

    # Define the model seed configuration data
    model_seed_config = OrchestratorConfig(
        username=user,
        password=password,
        num_forecast_years=cfg.get('numForecastYears'),
        num_historical_years=cfg.get('numHistoricalYears'),
        start_date=cfg.get('startDate'),
        model_configs=[
            OrchestratorModelConfig(template_id=template_id,
                                    company_name=cfg.get('companyName'),
                                    ticker=cfg.get('ticker'),
                                    industry=cfg.get('industry'),
                                    start_period=cfg.get('startPeriod'),
                                    source=cfg.get('variables', {}).get(
                                        'INTERNAL_SOURCE', ''))
        ])
    return model_seed_config


def run_each_allow_fail(funcs) -> List[str]:
    """Each function is allowed to execute;
    if any Exceptions are thrown, they are caught
    and the associated error message stored.
    
    All funcs are executed in order.
    """
    fails = []
    for func in funcs:
        try:
            func()
        except Exception as err:
            logger.exception(err)
            fails.append(str(err))
    return fails


def workflow(nm: str):

    def real_decorator(function):

        def wrapper(*args, **kwargs):
            logger.info(f"RUNNING WORKFLOW: {nm}")
            return function(*args, **kwargs)

        return wrapper

    return real_decorator
