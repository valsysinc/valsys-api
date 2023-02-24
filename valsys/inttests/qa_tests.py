from typing import List

from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.inttests.runners import runners as Runners
from valsys.inttests.utils import gen_cell_identifier, gen_orch_config, workflow
from valsys.modeling.model.line_item import LineItem
from valsys.utils.logging import loggerIT
from valsys.utils.time import yesterday


def qa_script():

    return {
        'modelConfig': {
            'companyName': 'Pepsi',
            'ticker': 'PEP',
            'templateName': 'dcf-standard',
            'numForecastYears': 5,
            'numHistoricalYears': 5,
            'industry': 'RETAIL-EATING \u0026 DRINKING PLACES',
            'startPeriod': 2019,
            'startDate': yesterday(),
        },
        'steps': [{
            'type': 'edit_formula',
            'startingModule': 'DCF',
            'targetLineItem': 'EBIT Margin',
            'targetCellPeriod': '2020',
            'originalCellFormula':
            'INTERPERCENT(2019, [DCF[EBIT Margin[2019]]], 2020, 2024, [DCF Drivers[Industry average EBIT margin[2020]]])',
            'originalCellValue': '0.1590030467086554',
            'newCellFormula':
            'AVERAGE([DCF[EBIT Margin[2015]]]:[DCF[EBIT Margin[2019]]])',
            'newCellValue': '0.1526595564601617',
        }, {
            'type': 'edit_line_item',
            'startingModule': 'Operating Income',
            'targetLineItem': 'Operating Profit',
            'targetCellPeriod': '2015',
            'originalCellFormula': '8353000000',
            'originalCellValue': 8353000000.0,
            "newCellFormula":
            "[Operating Income[Gross profit[2015]]]-SUM([Operating Income[Selling general and administrative expenses[2015]]],[Operating Income[Venezuela impairment charges[2015]]],[Operating Income[Amortization of intangible assets[2015]]])",
            "newCellValue": 8353000000.0,
            "newLineItem": {
                "targetLineItem":
                "Adj EBIT",
                'startingModule':
                'Operating Income',
                'targetCellPeriod':
                '2015',
                'newCellValue':
                9712000000.0,
                'originalCellValue':
                0.0,
                "newCellFormula":
                "SUM([Operating Income[Operating Profit[2015]]],[Operating Income[Venezuela impairment charges[2015]]])"
            }
        }, {
            'type':
            'add_module',
            'parentModule':
            'DCF',
            'newModuleName':
            "Geographic Disaggregation",
            'newLineItems':
            ['United States', 'United Kingdom', 'Other', 'Total'],
            'factEdits': [{
                'lineItem': 'United States',
                'fact': '[Geographic Disaggregation[United States[2015]]]',
                'inputValue': 123456789,
                'formula': '123456789',
                'expectedValue': 123456789
            }, {
                'lineItem': 'United Kingdom',
                'fact': '[Geographic Disaggregation[United Kingdom[2015]]]',
                'formula':
                '[Geographic Disaggregation[United States[2015]]]/2',
                'expectedValue': 61728394.5
            }, {
                'lineItem': 'United Kingdom',
                'fact': '[Geographic Disaggregation[United Kingdom[2016]]]',
                'formula':
                '[Geographic Disaggregation[United Kingdom[2015]]]*1.05',
                'expectedValue': 64814814.225
            }, {
                'lineItem': 'Total',
                'fact': '[Geographic Disaggregation[Total[2015]]]',
                'formula':
                '[Geographic Disaggregation[United States[2015]]] +[Geographic Disaggregation[United Kingdom[2015]]]',
                'expectedValue': 185185183.5
            }, {
                'lineItem': 'Other',
                'fact': '[Geographic Disaggregation[Other[2015]]]',
                'formula': '[Geographic Disaggregation[Total[2015]]] *1.2',
                'expectedValue': 222222220.2
            }]
        }, {
            'type': 'rename_line_item',
            'parentModule': 'Geographic Disaggregation',
            'originalLineItemName': "Total",
            'newLineItemName': 'abcdefg',
            'checkingLineItem': {
                'name': 'Other',
                'fact': '[Geographic Disaggregation[Other[2015]]]',
                'formula': '[Geographic Disaggregation[abcdefg[2015]]] *1.2',
                'originalFormula':
                '[Geographic Disaggregation[Total[2015]]] *1.2'
            }
        }],
    }


def run_qa_edit_formula(model_id: str, edit_formula_config):
    model = Runners.run_pull_model(model_id)
    module = model.pull_module_by_name(edit_formula_config['startingModule'])

    tcid = gen_cell_identifier(edit_formula_config)
    li = module.pull_item_by_name(edit_formula_config['targetLineItem'])
    Runners.run_edit_formula(
        model.uid,
        model.first_case_id,
        fact=li.pull_fact_by_identifier(tcid),
        original_formula=edit_formula_config['originalCellFormula'],
        new_formula=edit_formula_config['newCellFormula'],
        original_value=edit_formula_config['originalCellValue'],
        new_value=edit_formula_config['newCellValue'])
    Runners.run_recalculate_model(model.uid)

    #TODO
    # obtain implied premium value
    # recalc
    # obtain implied premium value (different to above)


def run_qa_add_line_item(model_id: str, config):
    model = Runners.run_pull_model(model_id)

    opinc = model.pull_module_by_name(config['startingModule'])
    line_item = opinc.pull_item_by_name(config['targetLineItem'])
    ticd = gen_cell_identifier(config)
    Runners.run_edit_formula(model.uid,
                             model.first_case_id,
                             fact=line_item.pull_fact_by_identifier(ticd),
                             original_value=config['originalCellValue'],
                             original_formula=config['originalCellFormula'],
                             new_formula=config['newCellFormula'],
                             new_value=config['newCellValue'])
    nli_config = config['newLineItem']
    nli = Runners.run_add_line_item(
        model.uid,
        model.first_case,
        opinc.uid,
        new_line_item_name=nli_config['targetLineItem'],
        new_line_item_order=line_item.order + 1)
    fid = gen_cell_identifier(nli_config)
    Runners.run_edit_formula(model_id=model.uid,
                             case_id=model.first_case_id,
                             fact=nli.pull_fact_by_identifier(fid),
                             new_formula=nli_config['newCellFormula'],
                             new_value=nli_config['newCellValue'],
                             original_value=nli_config['originalCellValue'])


def run_qa_add_module(model_id: str, config):
    model = Runners.run_pull_model(model_id)

    nm = Runners.run_add_child_module(model.uid,
                                      model.first_case_id,
                                      module_id=model.pull_module_by_name(
                                          config['parentModule']).uid,
                                      new_module_name=config['newModuleName'])
    order = 1
    nlis: List[LineItem] = []
    for new_line_item_name in config['newLineItems']:
        nli = Runners.run_add_line_item(model_id=model.uid,
                                        case=model.first_case,
                                        module_id=nm.uid,
                                        new_line_item_name=new_line_item_name,
                                        new_line_item_order=order)
        order += 1
        nlis.append(nli)

    for fact_edit in config['factEdits']:
        for li in nlis:
            if li.name == fact_edit['lineItem']:
                line_item = li
                break
        fact = line_item.pull_fact_by_identifier(fact_edit['fact'])
        if fact_edit.get('inputValue', '') != '':
            fact.value = fact_edit['inputValue']

        Runners.run_edit_formula(model_id=model.uid,
                                 case_id=model.first_case_id,
                                 fact=fact,
                                 new_formula=fact_edit.get('formula', ''),
                                 new_value=fact_edit.get('expectedValue', ''))


def run_qa_rename_line_item(model_id: str, config):
    model = Runners.run_pull_model(model_id)
    li = model.pull_line_item_by_name(config['parentModule'],
                                      config['originalLineItemName'])
    Runners.run_rename_line_item(model.uid, li, config['newLineItemName'])
    m2 = Runners.run_pull_model(model_id)
    li2 = m2.pull_line_item_by_name(config['parentModule'],
                                    config['checkingLineItem']['name'])
    f2 = li2.pull_fact_by_identifier(config['checkingLineItem']['fact'])
    assert f2.formula == config['checkingLineItem']['formula']

    # Now undo
    Runners.run_rename_line_item(model.uid, li, config['originalLineItemName'])
    m3 = Runners.run_pull_model(model_id)
    li3 = m3.pull_line_item_by_name(config['parentModule'],
                                    config['checkingLineItem']['name'])
    f3 = li3.pull_fact_by_identifier(config['checkingLineItem']['fact'])
    assert f3.formula == config['checkingLineItem']['originalFormula']


@workflow('qa tests')
def run_qa_script():

    qa_flow = qa_script()

    # Import the class for the model seed configuration data
    user, password = API_USERNAME, API_PASSWORD

    # Define the model seed configuration data
    model_seed_config = gen_orch_config(qa_flow.get('modelConfig'), user,
                                        password)

    # Spawn the model and obtain the modelID
    mid = Runners.run_spawn_single_model(model_seed_config)
    model = Runners.run_pull_model(mid)

    steps = {
        'edit_formula': run_qa_edit_formula,
        'edit_line_item': run_qa_add_line_item,
        'add_module': run_qa_add_module,
        'rename_line_item': run_qa_rename_line_item
    }

    for step_config in qa_flow['steps']:
        steps[step_config.get('type')](model.uid, step_config)
