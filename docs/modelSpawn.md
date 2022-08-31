# Model spawning

Models can be spawned on the valsys system in a variety of ways. This page explains a few of the common usecases.

## Using the workflow
This is a pre-defined set of actions which will be executed given the provided configuration data. The workflow is as follows:

1)  **Spawn a set of models based on a collection of tickers.** Collection of lists of tickers, each of which will all have the same `templateName`, `histPeriod`, `projPeriod`, `tags`, and `emails` (the `emails` are the list of emails of users with whom the models are shared).


2) **Populate the spawned models with additional modules.** Each model can be populated with different modules (based on a parent module), each with given line items, each of which can be formatted. Each fact (indexed by period) can have its formula provided.

The workflow requires a configuration; the structure of the configuration is explained below.

The spawn process can be started in two ways: via the command line, or via a python function call.

### Run via code
If you have a config file on disk use the `run_spawn_models_from_file` function, and pass the full path to file as an argument
```python
from valsys.workflows.service import run_spawn_models_from_file
run_spawn_models_from_file('config_file.json')
```

Alternatively, if you have the configuration in memory as a dict, then use the `run_spawn_models` function (passing the config dict as an argument):
```python
from valsys.workflows.service import run_spawn_models

config = {"spawnModelsConfig":[...],"populateModulesConfig":[...]}

run_spawn_models(config)
```



### Run via command line
The valsys library can be used from source via a command line interface (CLI).

This works by providing (via command line arguments) the path to a configuration file to the `main.py` python entry point:
```
python main.py --spawn assets/example_input.json
```



## Example input configuration
This provides a valid example of a configuration file which can be passed to the spawner CLI.
```json linenums="1"
{
    "spawnModelsConfig": [
        {
            "tickers": [
                {
                    "ticker": "SBUX",
                    "source": "dataSource|SBUX_US|jp"
                }
            ],
            "templateName": "dcf-standard",
            "numForecastYears": 2,
            "numHistoricalYears": 3,
            "tags": [
                "t1"
            ],
            "emails": [
                "jack.fuller@valsys.io"
            ]
        },
        {
            "tickers": [
                {
                    "ticker": "BYND",
                    "source": "dataSource|BYND_US|jp"
                }
            ],
            "templateName": "dcf-standard",
            "numForecastYears": 2,
            "numHistoricalYears": 3,
            "tags": [
                "t2"
            ],
            "emails": []
        }
    ],
    "populateModulesConfig": [
        {
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
                    "order": 1,
                    "formulaEdits": [
                        {
                            "periodName": "",
                            "periodYear": "2019",
                            "formula": "5*2"
                        }
                    ]
                },
                {
                    "name": "line item 2",
                    "order": 2,
                    "formulaEdits": [
                        {
                            "periodName": "",
                            "periodYear": "2018",
                            "formula": "1+2"
                        }
                    ]
                }
            ]
        },
        {
            "tickers": [
                "BYND"
            ],
            "parentModuleName": "Income Statement",
            "moduleName": "A new module",
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
                    "order": 1,
                    "formulaEdits": [
                        {
                            "periodName": "",
                            "periodYear": "2019",
                            "formula": "5*2"
                        }
                    ]
                },
                {
                    "name": "line item 2",
                    "order": 2,
                    "formulaEdits": [
                        {
                            "periodName": "",
                            "periodYear": "2018",
                            "formula": "1+2"
                        }
                    ]
                }
            ]
        }
    ]
}
```
There are two main chunks of config:

* `spawnModelsConfig` which controls the overal models to be spawned,
* `populateModulesConfig` which controls the module population of the models.

### `spawnModelsConfig`
A list of model configurations, where every ticker in a given configuration chunk will be configured identically. 

The fields which can be configured are:

* `tickers` A list of tickers to whom this configuration applies
* `templateName` The name of the template (invalid entries will have errors thrown)
* `numForecastYears` The number of forecast years
* `numHistoricalYears` The number of historical years
* `tags` A list of tags which will be applied to the models
* `emails` A list of user emails to whom the models will be shared

By default,

* `periodType` is set to `ANNUAL`
* `startDate` is set the current date/time

### `populateModulesConfig`
A list of module configurations, where every ticker in a given configuration chunk will be configured identically. This will add a child module to a parent module in the model.

The fields which can be configured are:

* `tickers` A list of tickers to whom this configuration applies
* `parentModuleName` The name of the parent module to add the child onto.
* `moduleName` The name of the new module
* `keyMetricsConfig` Information regarding  formatting of certain key line items which may (or may not) exist in the module; Any line item whose name appears in the `metrics` list will be formatted according to `format`.
* `lineItems` A list of line items which will be added to the module. A line item is specified by its `name`, `order` inside the module, and a list of `formulaEdits`: these are a list of data used to identify which formulae to change/add.

## Manual configuration

Finally, it is possible to construct custom configuration objects.

It may be the case that some other routine provides a list of model seeds; the key thing is that it contains data which can be interpreted in the following way
```python linenums="1"
# Example model seed data structure
from dataclasses import dataclass
@dataclass
class SampleModelSeed:
    companyName: str
    ticker: str
    template_id: str
    IndustryGroup: str
    fiscalYear: str
    source: str
```
Using this data structure we then assemble a list of `SampleModelSeed`s
```python linenums="1"
model_seeds = [
    SampleModelSeed(companyName='STARBUCKS CORP',
                    ticker='SBUX',
                    IndustryGroup='RETAIL-EATING & DRINKING PLACES',
                    template_id='d87b8446-38a1-4fd4-ad71-a40c3ef77b0f',
                    fiscalYear=2019,
                    source='SBUX_US|JP')
]

```
We are now in a position to create the full `OrchestratorConfig` object; we must also provide the number of historical and forecast years:
```python linenums="1"
import datetime
from valsys.seeds.models import OrchestratorConfig

# Create an orchestrator config object
orchestrator_configuration = OrchestratorConfig(
    num_forecast_years=11,
    num_historical_years=5,
    start_date=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
    period_type='ANNUAL')

# Add the model seeds to the orchestrator config
for row in model_seeds:
    orchestrator_configuration.add_model_config(
        company_name=row.companyName,
        ticker=row.ticker,
        template_id=row.template_id,
        industry=row.IndustryGroup,
        start_period=row.fiscalYear,
        source=row.source,
    )
```
Now that the configuration object has been fully constructed, it can be passed to a function to spawn the models, from which the spawned modelIDs can be extracted
```python linenums="1"
from valsys.spawn.service import orchestrate_model_spawns

# Pass the orchestrator config to be spawned
model_spawns = orchestrate_model_spawns(orchestrator_configuration)

# Collect together a list of modelIDs that successfully spawned
model_ids = []
for m in model_spawns:
    if m.spawned:
        model_ids.append(m.model_id)
```

Below is a complete list of configurable options for the `add_model_config` method.
:::valsys.seeds.models.OrchestratorConfig.add_model_config