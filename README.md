![alt text](coverage.svg "Coverage")

# Valsys API library

Purpose: library to build and interact with Valsys models via the API. See our [documentation](https://valsysinc.github.io/valsys-api/).

## Installation
### **Recommended**: installation via `pip`
For this, we recommend that you are in a virtual environment (see [getting started](https://valsysinc.github.io/valsys-api/) for ideas on how to do this); there is a requirement that you have python `>=3.6` installed. Assuming that you are in a virtual environment, the library can be installed via
```
pip install git+https://github.com/valsysinc/valsys-api
```

Once done, please see the [documentation](`https://valsysinc.github.io/valsys-api/`) to find out how to use the library.

Specific versions of the library can be installed via
```
pip install git+https://github.com/valsysinc/valsys-api@v0.4.3
```
where `v0.4.3` is the git tag of the required version (these can be found on the [github](https://github.com/valsysinc/valsys-api/tags) repo)
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

## Integration tests
This library can be used to run integration tests against the Valsys Modeling service.
Invoke via
```
python main.py --inttests <VALSYS_API_SOCKET> <VALSYS_API_SERVER> <VALSYS_API_USER> <VALSYS_API_PASSWORD>
```
The ordering of these parameters is important.