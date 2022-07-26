# Getting started


From a Jupyter notebook, connect to a python kernel (recommended that its a virtual environment, rather than the global python kernel). Install the valsys python package from within a cell via
```python
!pip install git+https://github.com/valsysinc/valsys-api
```

## Login
Once the library has been installed (e.g., via `pip`), the first task is to login.
```python
from valsys.admin import login
login()
```
Below we provide a screenshot of a jupyter notebook showing the expected screen and output.

![](images/jupyter_login.png "Jupyter login")