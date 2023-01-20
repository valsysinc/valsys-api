import datetime

from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.inttests.utils import gen_orch_config, workflow
from valsys.utils.logging import loggerIT
from valsys.inttests.runners import runners as Runners


def qa_script():

    starting_date = (datetime.datetime.utcnow() -
                     datetime.timedelta(days=1)).isoformat() + "Z"
    return {
        'modelConfig': {
            'companyName': 'Pepsi',
            'ticker': 'PEP',
            'templateName': 'dcf-standard',
            'numForecastYears': 5,
            'numHistoricalYears': 5,
            'industry': 'RETAIL-EATING \u0026 DRINKING PLACES',
            'startPeriod': 2019,
            'startDate': starting_date,
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


@workflow('qa tests')
def run_qa_script():

    qa_flow = qa_script()

    # Import the class for the model seed configuration data
    user, password = API_USERNAME, API_PASSWORD

    # Define the model seed configuration data
    model_seed_config = gen_orch_config(qa_flow.get('modelConfig'), user,
                                        password)

    # Spawn the model and obtain the modelID
    mid = Runners.run_spawn_model(model_seed_config)[0].model_id
    model = Runners.run_pull_model(mid)
    edit_formula_config = qa_flow['steps'][0]
    module = model.pull_module_by_name(edit_formula_config['startingModule'])

    tcid = f"[{edit_formula_config['startingModule']}[{edit_formula_config['targetLineItem']}[{edit_formula_config['targetCellPeriod']}]]]"
    loggerIT.info(
        f"searching for fact={tcid} in line item={edit_formula_config['targetLineItem']}"
    )

    li = module.pull_item_by_name(edit_formula_config['targetLineItem'])
    fact = li.pull_fact_by_identifier(tcid)
    loggerIT.info(
        f"editing fact formula from {edit_formula_config['originalCellFormula']} to {edit_formula_config['newCellFormula']}"
    )
    Runners.run_edit_formula(
        mid,
        model.first_case_id,
        fact,
        original_formula=edit_formula_config['originalCellFormula'],
        new_formula=edit_formula_config['newCellFormula'],
        original_value=edit_formula_config['originalCellValue'],
        new_value=edit_formula_config['newCellValue'])
    loggerIT.info(f"fact found: value {fact.value}")

    Runners.run_recalculate_model(model.uid)

    #TODO
    # obtain implied premium value
    # recalc
    # obtain implied premium value (different to above)

    return mid
