import os
from functools import wraps
from time import time
from valsys.utils import logger
LOG_TIME = False


def read_env(varn, required=True):
    """Read a variable from the environment.

    If `required=True`, then a `ValueError` is raised
    if the variable cannot be found.
    Oetherwise, the variable or `None` is returned."""
    var = os.getenv(varn)
    if var is None and required is True:
        raise ValueError(f'need to have {varn} environment variable')
    return var


def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        time_info = {
            'function': f.__name__,
            'elapsed': te-ts,
            'units': 's'
        }
        if LOG_TIME:
            logger.info(time_info)
        return result
    return wrap
