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


def assert_equal(v1, v2, desc=''):
    try:
        assert v1 == v2
    except AssertionError as err:
        logger.warning(f'{desc}: expected {v1} and {v2} to be equal')


def assert_not_none(v, desc=''):
    try:
        assert v is not None
    except AssertionError as err:
        logger.warning(f'wanted {desc} to be not None')