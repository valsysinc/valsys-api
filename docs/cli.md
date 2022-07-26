# Command line interface
The valsys library can be used from source via a command line interface (CLI).

This works by providing (via command line arguments) the path to a configuration file to the `main.py` python entry point:
```
python main.py --spawn assets/example_input.json
```
The above is an example input configuration file which should be inspected to understand whats required. See below.

This is a pre-defined set of actions which will be executed given the provided configuration data. The workflow is as follows:

1)  **Spawn a set of models based off a collection of tickers.** Collection of lists of tickers, each of which will all have the same `templateName`, `histPeriod`, `projPeriod`, `tags`, and `emails` (the `emails` are the list of emails of users with whom the models are shared).


2) **Populate the spawned models with modules.** Each model can be populated with different modules (based off a parent module), each with given line items, each of which can be formatted. Each fact (indexed by period) can have its formula provided.

## Example input configuration
This provides a valid example of a configuration file which can be passed to the spawner CLI.
```json linenums="1"
{
    "spawnModelsConfig": [
        {
            "tickers": [
                "SBUX"
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
                "BYND"
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