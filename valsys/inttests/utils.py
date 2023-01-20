from valsys.seeds.models import OrchestratorConfig, OrchestratorModelConfig
from valsys.seeds.loader import SeedsLoader


def gen_orch_config(cfg, user, password):

    template_id = SeedsLoader.template_id_by_name(cfg.get('templateName'))

    # Define the model seed configuration data
    model_seed_config = OrchestratorConfig(
        username=user,
        password=password,
        num_forecast_years=cfg.get('numForecastYears'),
        num_historical_years=cfg.get('numHistoricalYears'),
        start_date=cfg.get('startDate'),
        model_configs=[
            OrchestratorModelConfig(
                template_id=template_id,
                company_name=cfg.get('companyName'),
                ticker=cfg.get('ticker'),
                industry=cfg.get('industry'),
                start_period=cfg.get('startPeriod'),
            )
        ])
    return model_seed_config
