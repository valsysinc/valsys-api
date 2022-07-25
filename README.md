# Valsys API library

Purpose: library to spawn and populate Valsys models via the API.

## Installation
### **Recommended**: installation via `pip`
For this, recommend that you're in a virtual environment; there is a requirement that you have python `>=3.6` installed.
```
pip install git+https://github.com/valsysinc/valsys-api
```
The first time you use the system you'll have to `login`: this stores your Valsys credentials for use in authenticating with the Valsys API. In a python script (e.g., directly in the command line, inside a `Jupyter` notebook, or the repl), execute
```python
from valsys.admin import login
login()
```
This will have to be done whenever your password changes.
### Installation via source
This assumes you have some system python version. 
#### Mac/linux
On a linux-type system, execute
```
make install
```
This will create a python virtual environment and install neccesary python dependencies.

Finally, you will need to log into the valsys system; this allows authentication of API requests. To do so execute
```
make login
```

### Windows
* Have git installed https://git-scm.com/download/win
* Download python https://www.python.org/downloads/

From within powershell,
```
set-executionpolicy RemoteSigned # can only run as admin
python -m venv .venv
.venv\Scripts\activate.ps1
pip install -r requirements.txt
```
```
$Env:VALSYS_API_BUILD='test'
```
## Usage
Once installed, start the python environment via
```
source .venv/bin/activate
```
If your password changes, ensure you re-execute `make login`.

The library can be used in a few ways: 
* via a CLI,
* as a library of functions.

Detailed documentation on both of these use cases can be found [here](https://valsysinc.github.io/valsys-api/).

## Docserver
To see the docs locally,
```
make docserver
```
then visit `http://localhost:8989/` in a browser.

To see the public-facing docs, visit `https://valsysinc.github.io/valsys-api/`