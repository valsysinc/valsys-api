# Valsys API library

Purpose: library to spawn and populate Valsys models via the API.



## Installation
This assumes you have some system python version. On a linux-type system, execute
```
make install
```
This will create a python virtual environment, install necceasry python dependencies, and create a template environment file.

Note that the test env template will be copied and will contain all variables required (**health warning**: any existing config in that `.env` file will be copied into `env/.env.bak`).

## Usage
The library can be used in a few ways: 1) via a CLI, 2) as a library of functions.

Once installed, start the python environment via
```
source .venv/bin/activate
```

### CLI
The valsys library can be used from source via a CLI.

This works by providing (via command line arguments) the path to a configuration file to the `main.py` python entry point:
```
python main.py assets/example_input.json
```
The above is an example input configuration file which should be inspected to understand whats required.

This is a pre-defined set of actions which will be executed given the provided configuration data. The workflow is as follows:

1)  **Spawn a set of models based off a collection of tickers.** Collection of lists of tickers, each of which will all have the same `templateName`, `histPeriod`, `projPeriod`, `tags`, and `emails` (the `emails` are the list of emails of users with whom the models are shared).


2) **Populate the spawned models with modules.** Each model can be populated with different modules (based off a parent module), each with given line items, each of which can be formatted. Each fact (indexed by period) can have its formula provided.

## Docserver
execute
```
markdownserver
```
then visit `http://localhost:8009/docs/main.md` in a browser.