from valsys.utils import loggerIT as logger

from valsys.inttests.workflows import run_spawn_model, run_pull_model, run_edit_formula
from valsys.inttests.workflows import run_tag_line_item, run_add_line_item, run_filter_user_models
from valsys.inttests.workflows import run_pull_model_datasources, run_pull_model_information, run_remove_module
from valsys.inttests.workflows import run_add_child_module, run_recalculate_model, run_edit_format, run_delete_line_item
from valsys.inttests.workflows import run_rename_module
from valsys.config.config import BASE_SCK, BASE_URL


def run_workflows():
    logger.info('running integration tests')
    logger.info(f'modeling service HTTP URL:{BASE_URL}')
    logger.info(f'modeling service SOCK URL:{BASE_SCK}')

    spawned_models = run_spawn_model()
    model_id = spawned_models[0].model_id

    model = run_pull_model(model_id)
    first_case_id = model.first_case_id
    first_case = model.pull_case_by_id(first_case_id)
    module_id = first_case.first_module.uid

    new_module = run_add_child_module(model_id, first_case_id, module_id)

    run_recalculate_model(model_id)
    run_edit_formula(model_id,
                     first_case_id,
                     fact=model.first_case.first_module.line_items[0].facts[0])
    run_edit_format(model_id,
                    first_case_id,
                    fact=model.first_case.first_module.line_items[0].facts[0])
    run_tag_line_item(
        model_id, line_item_id=model.first_case.first_module.line_items[0].uid)
    run_add_line_item(model_id, first_case, module_id)
    run_pull_model_information(model_id)
    run_pull_model_datasources(model_id)
    run_remove_module(model_id, new_module.uid)
    run_filter_user_models(model_id)
    lid = len(model.first_case.first_module.line_items) - 1
    run_delete_line_item(model_id, module_id,
                         model.first_case.first_module.line_items[lid].uid)
    #TODO: make this test changing the name of a different module
    # to a modules name that currently exists.
    run_rename_module(model_id, module_id, 'new name!')
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


def wait_then_run():
    import time
    from valsys.modeling.service import health
    maxtries = 13
    sleep_time_sec = 0.1
    sleep_multfac = 2

    ntries = 1
    while True:
        try:
            logger.info(
                f'connecting to modeling service; trying {ntries}/{maxtries}')
            h = health()
            if h.get('status') == 'success':
                logger.info('modeling ok')
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
