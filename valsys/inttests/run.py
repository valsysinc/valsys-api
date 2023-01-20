import sys
import time
from valsys.utils import loggerIT as logger
from valsys.config.config import BASE_SCK, BASE_URL
from valsys.inttests.workflows import workflows


def run_workflows():
    logger.info('running integration tests')
    logger.info(f'modeling service HTTP URL:{BASE_URL}')
    logger.info(f'modeling service SOCK URL:{BASE_SCK}')
    try:
        workflows()
    except Exception as err:
        logger.info(f'FAILED: {str(err)}')

        sys.exit(1)

    logger.info('integration tests passed ok')


def wait_then_run(func=None):
    from valsys.modeling.service import health
    maxtries = 13
    sleep_time_sec = 0.1
    sleep_multfac = 2

    ntries = 1
    if func is None:
        func = run_workflows
    while True:
        try:
            logger.info(
                f'connecting to modeling service; trying {ntries}/{maxtries}')
            h = health()
            if h.get('status') == 'success':
                logger.info('modeling ok')
                func()
                break
        except Exception:
            pass

        ntries += 1
        logger.info(f"pause {sleep_time_sec}s")
        time.sleep(sleep_time_sec)
        sleep_time_sec *= sleep_multfac
        if ntries > maxtries:
            logger.info(
                f"could not connect to modeling service after {ntries} times.")
            break
