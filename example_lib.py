from valsys import ValsysSpawn, ModelSpawnConfig, PopulateModulesConfig

# Define configuration
model_spawn_config_json = {
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
}

module_spawn_config_json = {
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
model_spawn_config_obj = ModelSpawnConfig.from_json(model_spawn_config_json)

# Use the config object to spawn models.
# Returns a SpawnerProgress object: this holds information
# about which models succesfully spawned.
r = ValsysSpawn.spawn_models(model_spawn_config_obj)

# Collect together inputs required to add modules to newly created models.
# Note that we pass in the model ids for the newly spawned models (these are
# only the successful ones).
pmc = PopulateModulesConfig.from_json(model_ids=r.spawned_model_ids,
                                      config=module_spawn_config_json)

# Add modules to newly created models, according to the provided input configuration.
ValsysSpawn.populate_modules(pmc)
