# Getting started
## Create a python virtual environment
We recommended that you install the `valsys` library into a python virtual (local) environment, rather than into the global python environment. This requires you to have a system-wide installation of `python` (below we assume that your version of `python` is version `3.6` or later.). Other environment management systems are available.

To create a python virtual environment in the current directory, execute
```
python -m venv .venv
```
The activation of the virtual environment is slightly different on windows and mac:

* If on windows, use
```
.venv\Scripts\activate.ps1
```
* If on linux/mac, use
```
source .venv/bin/activate
```
## Installing the `valsys` package
Now that you have an active virtual environment, install the `valsys` python package into your environment via
```python
pip install git+https://github.com/valsysinc/valsys-api
```
Any other packages you require (e.g., `spark`, or `numpy`) will also need to be installed into the environment

## Environment setup
To effectively use the library certain environment variables are required. 
To do anything, put the following into the command line
```bash
export VALSYS_API_BUILD=local
```

More environment variables are required; these can be set in two ways: first via `login` process which guides you through the process, secondly via directly setting environment variables (if you are unsure as to which applies to your situation, contact valsys support).
### Login
Once the library has been installed, the first task is to login. From a python script (e.g., in the repl, or a jupyter notebook), execute
```python linenums="1"
from valsys.admin import login
login()
```
It is useful to put the above into a local script called `login.py` or something of that nature.

You will be prompted to enter the following information:

* **Valsys host**: the base part of the valsys url (if unsure, contact valsys support)
* **Valsys protocol**: whether using `http` or `https`. 
* **Valsys username**: this is the username used to login to the valsys system 
* **Valsys password**: this is the password used to login to the valsys system

The login process will attempt to authenticate with these pieces of information.

Below we provide a screenshot of a jupyter notebook showing the expected screen and output.

![](images/jupyter_login.png "Jupyter login")

### Environment variables
If the `login` function does not works for your system, you will need to manually configure the following environment variables:

* `VALSYS_API_BUILD`: this is your company identifier (contact valsys support to find this value)
* `VALSYS_API_SOCKET`: the socket address (e.g., `wss://dev-api.valsys.io`)
* `VALSYS_API_SERVER`: the http(s) server address (e.g., `https://dev-api.valsys.io`)
* `VALSYS_API_USER`: the username used to log into the valsys system
* `VALSYS_API_PASSWORD`: the password used to log into the valsys system

Your operating system or IDE will dictate the best method for setting these variables.

