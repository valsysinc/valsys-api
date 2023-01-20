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


def qa_script():
    import datetime
    sd = (datetime.datetime.utcnow() -
          datetime.timedelta(days=1)).isoformat() + "Z"
    return {
        'modelConfig': {
            'templateName': 'dcf-standard',
            'companyName': 'Pepsi',
            'ticker': 'PEP',
            'numHistoricalYears': 5,
            'numForecastYears': 5,
            'industry': 'RETAIL-EATING \u0026 DRINKING PLACES',
            'startPeriod': 2019,
            'startDate': sd,
        },
        'steps': [{
            'type': 'edit_formula',
            'startingModule': 'DCF',
            'targetLineItem': 'EBIT Margin',
            'targetCellPeriod': '2020',
            'originalCellFormula':
            'INTERPERCENT(2019, [DCF[EBIT Margin[2019]]], 2020, 2024, [DCF Drivers[Industry average EBIT margin[2020]]])',
            'originalCellValue': 0.1590030467086554,
            'newCellFormula':
            'AVERAGE([DCF[EBIT Margin[2015]]]:[DCF[EBIT Margin[2019]]])',
            'newCellValue': 0.1526595564601617,
        }],
    }


def run_qa_script():
    from valsys.utils.logging import loggerIT
    qa_flow = qa_script()

    # Import the spawn_model function from the modeling service
    from valsys.modeling.service import spawn_model
    from valsys.config.config import API_PASSWORD, API_USERNAME
    from valsys.inttests.workflows import gen_orch_config
    # Import the class for the model seed configuration data
    user, password = API_USERNAME, API_PASSWORD

    # Define the model seed configuration data
    model_seed_config = gen_orch_config(qa_flow.get('modelConfig'), user,
                                        password)

    # Spawn the model and obtain the new modelID
    spawned_model_id = spawn_model(model_seed_config)
    assert isinstance(spawned_model_id, list)
    from valsys.modeling.service import pull_model, edit_formula, recalculate_model
    mid = spawned_model_id[0].model_id
    m = pull_model(mid)
    edit_formula_config = qa_flow['steps'][0]
    module = m.pull_module_by_name(edit_formula_config['startingModule'])
    edited_facts = []

    tcid = f"[{edit_formula_config['startingModule']}[{edit_formula_config['targetLineItem']}[{edit_formula_config['targetCellPeriod']}]]]"
    loggerIT.info(
        f"searching for {tcid} in line item {edit_formula_config['targetLineItem']}"
    )

    for li in module.line_items:
        if li.name == edit_formula_config['targetLineItem']:
            for fact in li.facts:
                if fact.identifier == tcid:
                    assert fact.formula == edit_formula_config[
                        'originalCellFormula']
                    assert fact.value == edit_formula_config[
                        'originalCellValue']
                    fact.formula = edit_formula_config['newCellFormula']
                    loggerIT.info(f"fact found: value {fact.value}")
                    edited_facts.append(fact)
                    break
    loggerIT.info(
        f"editing fact formula from {edit_formula_config['originalCellFormula']} to {edit_formula_config['newCellFormula']}"
    )
    ef = edit_formula(m.first_case_id, m.uid,
                      [ff.jsonify() for ff in edited_facts])
    for f in ef:
        if f.uid == edited_facts[0].uid:
            assert f.identifier == tcid
            assert f.value == edit_formula_config['newCellValue']
    loggerIT.info('recalculating model')
    recalculate_model(m.uid)

    #TODO
    # obtain implied premium value
    # recalc
    # obtain implied premium value (different to above)

    return spawned_model_id


def wait_then_run(func=None):
    import time
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
