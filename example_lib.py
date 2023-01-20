from valsys.spawn.service import ValsysSpawn
from valsys.spawn.models import ModelSpawnConfigs, PopulateModulesConfig

# Define configuration: list of dict's of configurations.
# Each dict is treated separetely, but everything in a given dict
# is treated the same (i.e., every ticker in the dict has the same templateName,
# but a different dict can use a different template name for other tickers.)
model_spawn_config_json = [{
    "tickers": ["PEP", "BYND"],
    "templateName": "dcf-standard",
    "histPeriod": 2,
    "projPeriod": 3,
    "tags": ["t1"],
    "emails": ["jack.fuller@valsys.io"]
}]

module_spawn_config_json = {
    "tickers": ["PEP"],
    "parentModuleName":
    "Income Statement",
    "moduleName":
    "Operating Model",
    "keyMetricsConfig": {
        "metrics": [
            "Revenue Growth, %", "Gross Margin, %", "SG&A / sales",
            "R&D / sales", "Capex / sales"
        ],
        "format": {
            "fontWeight": "bold",
            "fontStyle": "normal",
            "textAlign": "right",
            "textDecoration": "none",
            "valFormat": "Percentage",
            "unit": "Raw",
            "decimalPlaces": 1
        }
    },
    "lineItems": [{
        "name": "Revenue Growth, %",
        "order": 2
    }, {
        "name": "line item 2",
        "order": 1
    }]
}

# Turn the configuration json into a usable model config object
model_spawn_config_obj = ModelSpawnConfigs.from_json(model_spawn_config_json)

# Use the config object to spawn models.
# Returns a SpawnerProgress object: this holds information
# about which models succesfully spawned.
spawn_report = ValsysSpawn.spawn_models(model_spawn_config_obj)

# Collect a list of modelIDs for the successfully spawned models.
model_ids_for_ticker = spawn_report.spawned_model_ids_for_tickers(
    spawn_report.spawned_tickers)

# Collect together inputs required to add modules to newly created models.
# Note that we pass in the model ids for the newly spawned models (these are
# only the successful ones).
pmc = PopulateModulesConfig.from_json(config=module_spawn_config_json,
                                      model_ids=model_ids_for_ticker)

# Add modules to newly created models, according to the provided input configuration.
ValsysSpawn.populate_modules(pmc)
