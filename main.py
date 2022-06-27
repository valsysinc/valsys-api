import datetime
import json
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
# prop: model itself

######
from valsys.modeling.service import pull_case, pull_model_information


parent_module_name = "DCF"
new_module_name = "Operating Model"
key_metrics = [
    "Revenue Growth, %",
    "Gross Margin, %",
    "SG&A / sales",
    "R&D / sales",
    "Capex / sales",
]
key_metrics_format = {
    "fontWeight": "bold",
    "fontStyle": "normal",
    "textAlign": "right",
    "textDecoration": "none",
    "valFormat": "Percentage",
    "unit": "Raw",
    "decimalPlaces": 1,
}

for mi in spawner_report:
    if not mi.spawned:
        continue
    model_id = mi.model_id
    #   model_id = "0x21fa898"
    logger.info(f"processing model id: {model_id}, ticker: {mi.ticker}")
    case_id = pull_model_information(uid=model_id)
    case = pull_case(uid=case_id)
    continue

    root_module = case.pull_module(parent_module_name)

    if root_module is None:
        continue
    new_module = root_module.add_child_module(new_module_name, model_id, case_id)
    item_name, item_order = "item 1", 1
    item_obj = new_module.add_item(item_name, item_order, model_id, case_id)
    for km in key_metrics:
        for i, cell in enumerate(item_obj.facts):
            cell.fmt = json.dumps(key_metrics_format)
            item_obj.facts[i] = cell
        item_obj.edit_format(model_id, case_id)
