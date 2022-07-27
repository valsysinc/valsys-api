# Valsys API library

Purpose: library to build and interact with Valsys models via the API.

## Installation
### **Recommended**: installation via `pip`
For this, recommend that you're in a virtual environment (see [getting started](https://valsysinc.github.io/valsys-api/) for ideas on how to do this); there is a requirement that you have python `>=3.6` installed.
```
pip install git+https://github.com/valsysinc/valsys-api
```

Once done, please see the [documentation](`https://valsysinc.github.io/valsys-api/`) to find out how to use the library.
### Installation via source
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


## Docserver
To see the docs locally,
```
make docserver
```
then visit `http://localhost:8989/` in a browser.

