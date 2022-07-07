from valsys import ValsysSpawn, ModelSpawnConfig, PopulateModulesConfig
cfg = ModelSpawnConfig.from_json({
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
})

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
            "order": 0
        },
        {
            "name": "line item 2",
            "order": 1
        }
    ]
}
r = ValsysSpawn.spawn_models(cfg)
pmc = PopulateModulesConfig.from_json(model_ids=r.spawned_model_ids,
                                      config=module_spawn_config_json)
ValsysSpawn.populate_modules(pmc)
