from valsys.utils import loggerIT as logger


def runner(nm: str):

    def real_decorator(function):

        def wrapper(*args, **kwargs):
            logger.info(f"running: {nm}")
            return function(*args, **kwargs)

        return wrapper

    return real_decorator
