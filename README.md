# Valsys API library

Purpose: spawning & sharing models



## Installation
This assumes you have some system python version.
- Start a venv
```
python3 -m venv .venv
source .venv/bin/activate
```
- Install dependencies
```
pip install -r requirements.txt
```
- Set environment variables in `env/.env`; the required fields are
```
VALSYS_API_SERVER="http://localhost:5200"
VALSYS_API_SOCKET="wss://localhost:5200"
VALSYS_API_USER=<USERNAME>
VALSYS_API_PASSWORD=<PASSWORD>
```
If you run
```
cp env/.env.test env/.env
```
then the test env template will be copied and will contain all variables required (**health warning**: any existing config in that `.env` file will be blown away).

## Usage
The library can be used in a few ways: 1) via a CLI, 2) as a library of functions.
### CLI
The valsys library can be used from source via a CLI
```
python main.py assets/example_input.json
```
This is a pre-defined set of actions which will be executed given the provided configuration data.
The workflow is as follows:

1)  Spawn a set of models based off a collection of tickers. 

    * List of tickers which will all have the same `templateName`, `histPeriod`, `projPeriod`, `tags`, and `emails` (the `emails` are the list of emails with whom the models are shared).


2) Populate the spawned models with modules. Each model can be populated with different modules (based off a parent module), each with given line items, each of which can be formatted. Each fact (indexed by period) can have its formula provided.