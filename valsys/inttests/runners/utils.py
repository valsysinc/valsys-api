from typing import List, Any
from valsys.utils import loggerIT as logger


def runner(nm: str):

    def real_decorator(function):

        def wrapper(*args, **kwargs):
            logger.info(f"running: {nm}")
            try:
                res = function(*args, **kwargs)
            except Exception as err:
                logger.exception(err)
                logger.error(f"failed: {nm} {err}")
                raise

            return res

        return wrapper

    return real_decorator

def assert_contains(mstr:List[Any], tsts:List[Any], desc=''):
    for t in tsts:
        try:
            assert t in mstr
        except AssertionError:
            logger.warning(f'{desc}: expected {t} to be in {mstr}')
            raise

def assert_equal(v1, v2, desc=''):
    try:
        assert v1 == v2
    except AssertionError as err:
        logger.warning(f'{desc}: expected {v1} and {v2} to be equal')
        raise


def assert_true(v, desc=''):
    return assert_equal(v, True, desc)


def assert_false(v, desc=''):
    return assert_equal(v, False, desc)


def assert_not_none(v, desc=''):
    try:
        assert v is not None
    except AssertionError as err:
        logger.warning(f'wanted {desc} to be not None')
        raise


def assert_gt(v1, v2, desc=''):
    try:
        assert v1 > v2
    except AssertionError as err:
        logger.warning(f"{desc} expected {v1} > {v2}; err={str(err)}")
        raise
