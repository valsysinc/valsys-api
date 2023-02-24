import sys

from valsys.config.config import log_modeling_service_info
from valsys.inttests.integration_tests import run_integration_tests
from valsys.inttests.qa_tests import run_qa_script
from valsys.inttests.utils import run_each_allow_fail
from valsys.utils import loggerIT as logger


MSG_RUNNING_TESTS = 'running integration tests'
MSG_TESTS_FINISHED = 'tests finished'
MSG_TESTS_PASSED = 'integration tests passed ok'


def run_workflows(opts):
    logger.info(MSG_RUNNING_TESTS)
    log_modeling_service_info(logger.info)
    workflow_funcs = []
    if 'integration' in opts:
        workflow_funcs.append(run_integration_tests)
    if 'qa' in opts:
        workflow_funcs.append(run_qa_script)
    if len(workflow_funcs) == 0:
        workflow_funcs = [run_integration_tests, run_qa_script]
    fails = run_each_allow_fail(workflow_funcs)
    logger.info(MSG_TESTS_FINISHED)
    if len(fails) > 0:
        logger.info(f"FAILED: {', '.join(fails)}")
        sys.exit(1)

    logger.info(MSG_TESTS_PASSED)
