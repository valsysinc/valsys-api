from valsys import ValsysSpawn, ModelSpawnConfigs, PopulateModulesConfig

# Define configuration
model_spawn_config_json = [{
    "tickers": [
        "SBUX",
        "BYND"
    ],
    "templateName": "dcf-standard",
    "histPeriod": 2,
    "projPeriod": 3,
    "tags": [
        "t1"
    ],
    "emails": [
        "jack.fuller@valsys.io"
    ]
}]

module_spawn_config_json = {
    "tickers": [
        "SBUX"
    ],
    "parentModuleName": "Income Statement",
    "moduleName": "Operating Model",
    "keyMetricsConfig": {
        "metrics": [
            "Revenue Growth, %",
            "Gross Margin, %",
            "SG&A / sales",
            "R&D / sales",
            "Capex / sales"
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
    "lineItems": [
        {
            "name": "Revenue Growth, %",
            "order": 2
        },
        {
            "name": "line item 2",
            "order": 1
        }
    ]
}

# Turn the configuration json into a usable model config object
model_spawn_config_obj = ModelSpawnConfigs.from_json(model_spawn_config_json)

# Use the config object to spawn models.
# Returns a SpawnerProgress object: this holds information
# about which models succesfully spawned.
spawn_report = ValsysSpawn.spawn_models(model_spawn_config_obj)

# Collect a list of modelIDs for the successfully spawned models.
model_ids_for_ticker = spawn_report.spawned_model_ids_for_tickers(spawn_report.spawned_tickers)

# Collect together inputs required to add modules to newly created models.
# Note that we pass in the model ids for the newly spawned models (these are
# only the successful ones).
pmc = PopulateModulesConfig.from_json(config=module_spawn_config_json, model_ids=model_ids_for_ticker)

# Add modules to newly created models, according to the provided input configuration.
ValsysSpawn.populate_modules(pmc)
