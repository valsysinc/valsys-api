# Valsys API library

Purpose: library to build and interact with Valsys models via the API. See our [documentation](https://valsysinc.github.io/valsys-api/).

## Installation2
### **Recommended**: installation via `pip`
For this, we recommend that you are in a virtual environment (see [getting started](https://valsysinc.github.io/valsys-api/) for ideas on how to do this); there is a requirement that you have python `>=3.6` installed. Assuming that you are in a virtual environment, the library can be installed via
```
pip install git+https://github.com/valsysinc/valsys-api
```

Once done, please see the [documentation](`https://valsysinc.github.io/valsys-api/`) to find out how to use the library.
### **Advanced**: installation via source
For more advance use, the source code can be cloned locally (via `git clone https://github.com/valsysinc/valsys-api.git`) and interacted with directly. 

On a mac/linux system, execute
```
make install
```
This will create a python virtual environment and install neccesary python dependencies.

Finally, you will need to log into the valsys system; this allows authentication of API requests. To do so execute
```
make login
```


## Docserver
The documentation can be viewed locally by executing
```
make docserver
```
then visit `http://localhost:8989/` in a browser.

