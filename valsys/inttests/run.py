import sys
import time

from valsys.config.config import BASE_SCK, BASE_URL
from valsys.inttests.integration_tests import run_integration_tests
from valsys.inttests.qa_tests import run_qa_script
from valsys.inttests.utils import run_each_allow_fail
from valsys.modeling.service import health
from valsys.modeling.vars import Vars
from valsys.utils import loggerIT as logger


def run_workflows(opts):
    logger.info('running integration tests')
    logger.info(f'modeling service HTTP URL:{BASE_URL}')
    logger.info(f'modeling service SOCK URL:{BASE_SCK}')
    workflow_funcs = []
    if 'integration' in opts:
        workflow_funcs.append(run_integration_tests)
    if 'qa' in opts:
        workflow_funcs.append(run_qa_script)
    if len(workflow_funcs) == 0:
        workflow_funcs = [run_integration_tests, run_qa_script]
    fails = run_each_allow_fail(workflow_funcs)
    if len(fails) > 0:
        logger.info(f"FAILED: {', '.join(fails)}")
        sys.exit(1)

    logger.info('integration tests passed ok')


def wait_then_run_tests():

    maxtries = 13
    sleep_time_sec = 0.1
    sleep_multfac = 2

    ntries = 1

    while True:
        try:
            logger.info(
                f'connecting to modeling service; trying {ntries}/{maxtries}')
            h = health()
            if h.get('status') == Vars.SUCCESS:
                logger.info('connection to modeling service ok')
                run_workflows()
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
