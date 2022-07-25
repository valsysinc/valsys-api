# Valsys API library

Purpose: library to spawn and populate Valsys models via the API.



## Installation
This assumes you have some system python version. 

On a linux-type system, execute
```
make install
```
This will create a python virtual environment and install neccesary python dependencies.

Finally, you will need to log into the valsys system; this allows authentication of API requests. To do so execute
```
make login
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