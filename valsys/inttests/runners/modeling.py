import uuid
from copy import deepcopy
from typing import Dict, List

from valsys.inttests.runners import checkers as Check
from valsys.inttests.runners.utils import (
    assert_equal,
    assert_false,
    assert_gt,
    assert_not_none,
    assert_true,
    assert_contains,
    runner,
)
from valsys.modeling import service as Modeling
from valsys.modeling.model.case import Case
from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.model.model import Model
from valsys.utils.time import yesterday
from valsys.modeling.client.exceptions import ModelingServiceDeleteException


@runner('spawn model')
def run_spawn_model(model_config):
    """
    SPAWN A MODEL
    """
    # Spawn the model and obtain the new modelID
    spawned_model_id = Modeling.spawn_model(model_config)
    assert isinstance(spawned_model_id, list)
    return spawned_model_id


@runner('spawn single model')
def run_spawn_single_model(model_config) -> str:
    """
    SPAWN A SINGLE MODEL
    """
    return run_spawn_model(model_config)[0].model_id


@runner('pull model')
def run_pull_model(model_id: str) -> Model:
    return Modeling.pull_model(model_id)


@runner('edit formula')
def run_edit_formula(model_id: str,
                     case_id: str,
                     fact: Fact,
                     original_formula='',
                     new_formula='42',
                     original_value='',
                     new_value=''):
    assert_not_none(fact, 'fact exists')

    if original_formula != '':
        assert_equal(fact.formula, original_formula, 'original formula')

    if original_value != '':
        assert_equal(fact.value, original_value, 'original value')

    fact.formula = new_formula
    efs = Modeling.edit_formula(case_id, model_id,
                                [ff.jsonify() for ff in [fact]])
    found = False
    for f in efs:
        if f.uid == fact.uid:
            assert_equal(f.formula, new_formula, 'new formula')
            found = True
            if new_value != '':
                assert_equal(f.value, new_value, 'new value')
    assert found


@runner('edit format')
def run_edit_format(model_id: str, case_id: str, fact: Fact):
    from valsys.modeling.service import edit_format
    new_format = '{"thing":42, "valFormat":"Numeric"}'
    fact.fmt = new_format
    efs = edit_format(case_id, model_id, [ff.jsonify() for ff in [fact]])
    found = False
    for f in efs:
        if f.uid == fact.uid:
            assert f.fmt == new_format
            found = True
    assert found


@runner('tag line item')
def run_tag_line_item(model_id: str, line_item_id: str, common_tag='t4'):
    import uuid

    new_tags = [common_tag, str(uuid.uuid1())]
    tli = Modeling.tag_line_item(model_id, line_item_id, new_tags)
    assert tli.tags == new_tags


@runner('add line item')
def run_add_line_item(model_id: str,
                      case: Case,
                      module_id: str,
                      new_line_item_name=None,
                      new_line_item_order=None):
    from valsys.inttests.config import AddLineItemConfig
    new_line_item_name = new_line_item_name or AddLineItemConfig.NAME
    new_line_item_order = new_line_item_order or AddLineItemConfig.ORDER
    new_line_item = Modeling.add_line_item(case.uid, model_id, module_id,
                                           new_line_item_name,
                                           new_line_item_order)

    assert new_line_item.name == new_line_item_name
    assert new_line_item.order == new_line_item_order
    return new_line_item


@runner('remove line item')
def run_delete_line_item(model_id: str, module_id: str, line_item_id: str):

    original_model = Modeling.pull_model(model_id)
    original_module = original_model.pull_module(module_id)
    orig_num_line_items = len(original_module.line_items)
    original_model.pull_line_item(line_item_id)

    parent_module = Modeling.delete_line_item(model_id, module_id,
                                              line_item_id)
    assert parent_module.uid == module_id
    for l in parent_module.line_items:
        assert l.uid != line_item_id
    assert len(parent_module.line_items) == orig_num_line_items - 1
    modified_model = Modeling.pull_model(model_id)

    try:
        modified_model.pull_line_item(line_item_id)
    except Exception as err:
        assert "cannot find line item with id" in str(err)


@runner('filter user model')
def run_filter_user_model(model_id: str):
    ms = Modeling.filter_user_models()
    assert_gt(len(ms), 0, 'number of user models')

    found = False
    for m in ms:
        if m.uid == model_id:
            found = True
    assert_true(found, 'expected to find model uid in response')

    # given that the target UID was just created, targeting
    # models yesterday should give nothing.
    ys = Modeling.filter_user_models(max_date=yesterday())
    found = False
    for m in ys:
        if m.uid == model_id:
            found = True
    assert_false(found, 'expected to not find uid in response')


@runner('filter user model with fields')
def run_filter_user_model_with_fields(model_id, ticker):

    flds = [
        '[Capital expenditure (DCF)[LFY+1]]',
        '[Capital expenditure (DCF)[LFY-1]]'
    ]
    ms2 = Modeling.filter_user_models(fields=flds,
                                      filter_term=ticker,
                                      filter_on=['Ticker'])
    assert_gt(len(ms2), 0, 'results returned')
    for m in ms2:
        if m.model.uid == model_id:
            assert_equal(set(flds), set(m.fields.keys()), 'filtered fields')


@runner('delete models')
def run_delete_models(model_ids: List[str]):
    d = Modeling.delete_models(model_ids)
    for mid in model_ids:
        try:
            Modeling.pull_model(mid)
            raise AssertionError('should have errored out the pull')
        except Exception as err:
            pass


@runner('multi filters')
def run_multi_filters(base_config: Dict[str, str], user: str, password: str,
                      cgen):
    ncompany_names = 4
    company_name_base = base_config.get('companyName') + "-" + str(
        uuid.uuid1())
    company_names = [
        company_name_base + str(uuid.uuid1()) for _ in range(ncompany_names)
    ]
    spawned_model_ids = []
    for tkr in company_names:
        cfg = deepcopy(base_config)
        cfg['companyName'] = tkr
        spawned_model = run_spawn_model(
            cgen(cfg=cfg, user=user, password=password))
        spawned_model_ids.append(spawned_model[0].model_id)

    results = Modeling.filter_user_models(filter_term=company_name_base,
                                          filter_on=['Name'],
                                          tag_filter_type='or')

    assert set([m.model.company_name for m in results]) == set(company_names)
    assert_equal(len(results), len(company_names), 'number of models returned')

    run_delete_models(spawned_model_ids)
    results = Modeling.filter_user_models(filter_term=company_name_base,
                                          filter_on=['Name'],
                                          tag_filter_type='or')
    assert_equal(len(results), 0, 'no models')


@runner('pull model data sources')
def run_pull_model_datasources(model_id: str):
    ds = Modeling.pull_model_datasources(model_id)
    assert isinstance(ds, str)


@runner('pull model information')
def run_pull_model_information(model_id: str):
    return Modeling.pull_model_information(model_id)


@runner('add child module')
def run_add_child_module(model_id: str,
                         case_id: str,
                         module_id: str,
                         new_module_name="new Module"):

    new_module = Modeling.add_child_module(module_id, new_module_name,
                                           model_id, case_id)
    assert new_module.name == new_module_name
    return new_module


@runner('remove module')
def run_remove_module(model_id: str, module_id: str):
    from valsys.modeling.exceptions import RemoveModuleException

    # Before we do anything, pull the model and validate
    # that the target module actually exists
    original_model = Modeling.pull_model(model_id)
    original_model.pull_module(module_id)

    # Now delete the target module
    assert Modeling.remove_module(model_id, module_id)

    # Now validate that the target module doesnt exist.
    m = Modeling.pull_model(model_id)
    try:
        m.pull_module(module_id)
    except Exception as err:
        assert 'cannot find module with id' in str(err)

    # Just for fun, try and delete the module again;
    # it should fail.
    try:
        Modeling.remove_module(model_id, module_id)
    except RemoveModuleException:
        pass


@runner('recalculate model')
def run_recalculate_model(model_id: str, expect_facts=True):
    from valsys.modeling.service import recalculate_model
    rm = recalculate_model(model_id)
    if expect_facts:
        assert rm


@runner('rename module')
def run_rename_module(model_id: str, module_id: str, new_name: str):
    r = Modeling.rename_module(model_id, module_id, new_name)
    assert r.name == new_name
    r = Modeling.rename_module(model_id, module_id, new_name)


@runner('reorder module')
def run_reorder_module(model_id: str, module_id: str, line_item_id: str,
                       order: int):
    nm = Modeling.reorder_module(model_id, module_id, line_item_id, order)
    Check.order(nm, line_item_id, order)

    # Check that can reorder to its own position
    nm = Modeling.reorder_module(model_id, module_id, line_item_id, order)
    Check.order(nm, line_item_id, order)

    # Check cannot reorder to a negative position
    try:
        nm = Modeling.reorder_module(model_id, module_id, line_item_id, -1)
        Check.order(nm, line_item_id, -1)
    except Exception as err:
        assert 'invalid order' in str(err)

    # Check cannot reorder to an overly positive position
    try:
        nm = Modeling.reorder_module(model_id, module_id, line_item_id, 10000)
        Check.order(nm, line_item_id, 10000)
    except Exception as err:
        assert 'invalid order' in str(err)


@runner('rename line item')
def run_rename_line_item(model_id: str, line_item: LineItem,
                         new_line_item_name: str):
    line_item.name = new_line_item_name
    nli = Modeling.edit_line_items(model_id, [line_item])[0]

    assert nli.uid == line_item.uid
    assert nli.name == line_item.name


@runner('add column')
def run_add_column(model_id: str, module_id: str, new_period: float):
    nm = Modeling.add_column(model_id, module_id, new_period)
    Check.period(nm, new_period)

    # Now try to add again (the column that was just add):
    # it should fail
    try:
        Modeling.add_column(model_id, module_id, new_period)
    except Exception as err:
        assert 'suggested period is invalid' in str(err)


@runner('delete column')
def run_delete_column(model_id: str, module_id: str, period: float):
    rc = Modeling.delete_column(model_id, module_id, period)
    for line_item in rc.line_items:
        for fact in line_item.facts:
            assert fact.period != period

    # Now try to delete again (the column that was just deleted):
    # it should fail
    try:
        Modeling.delete_column(model_id, module_id, period)
    except Exception as err:
        assert 'suggested period is invalid' in str(err)


@runner('copy model')
def run_copy_model(model_id: str):
    nm = Modeling.copy_model(model_id)
    # TODO: modeling service has a bug whereby the
    # created at time of the new model is identical
    # to the original model. This is to be fixed.
    # Once fixed, this should be checked for in this test.
    # Ticket: MOD-6
    assert nm.uid != model_id
    return nm.uid


@runner('create group')
def run_create_group(model_ids: List[str], group_name: str):
    g = Modeling.create_group(model_ids, group_name)
    assert g.name == group_name
    assert_equal(set(g.model_ids), set(model_ids))
    return g


@runner('delete group')
def run_delete_model_group(group_id: str, expect_err=False):
    try:
        Modeling.delete_group(group_id)
        if expect_err:
            raise AssertionError('should have errored and didnt')
    except ModelingServiceDeleteException:
        if expect_err:
            return
        raise
    existing_groups = Modeling.pull_model_groups()
    for g in existing_groups:
        assert g.uid != group_id


@runner('execute simulation')
def run_execute_simulation(group_id: str, model_ids: List[str],
                           edits: List[Dict[str, str]],
                           output_variables: List[str], tag: str, lfy):
    s = Modeling.execute_simulation(group_id,
                                    model_ids,
                                    edits=edits,
                                    output_variables=output_variables,
                                    tag=tag)

    expected_fields = set([
        'Change in IRR', 'Current share price (DCF)',
        'Implied share price (DCF)', 'Ticker'
    ])

    assert_contains(s.group_fields, expected_fields,
                    'simulated expected fields')
    edited_periods = []
    for e in edits:
        p = int(lfy) + int(e['timePeriod'].replace('LFY', ''))
        edited_periods.append(
            (p, float(e['formula'].replace('$FORMULA * ', ''))))

    assert_equal(set(model_ids), set(sim.id for sim in s.simulation),
                 'model ids')
    simulated_models = []
    for l in s.simulation:
        model = Modeling.pull_model(l.id)
        m = {'uid': l.id, 'lis': []}
        for li in l.line_items:
            lid = li.uid
            assert tag in li.tags
            assert li.name in output_variables
            m['lis'].append(model.pull_line_item(lid))
        simulated_models.append(m)

    simulated_facts = []

    for f in simulated_models:
        for ll in f['lis']:
            for ff in ll.facts:
                fe = {
                    'factId': ff.uid,
                    'originalValue': ff.value,
                    'editExpected': False,
                    'edited': False
                }
                for p, e in edited_periods:
                    if ff.period == p:
                        fe['editExpected'] = True
                        # NOTE: this is where we assume that the formula is a simple
                        # multiplication...
                        fe['expectedNewValue'] = ff.value * e
                simulated_facts.append(fe)

    for sim in s.simulation:
        for ll in sim.line_items:
            for f in ll.facts:
                tidx = -1
                for idx, ff in enumerate(simulated_facts):
                    if ff['factId'] == f.uid:
                        tidx = idx
                        break
                if tidx == -1:
                    raise Exception('not found')
                for p, e in edited_periods:
                    if f.period == p:
                        simulated_facts[tidx]['edited'] = True
                        simulated_facts[tidx]['newValue'] = f.value

    if len(edits) > 0:
        assert len(simulated_facts) > 0
    for f in simulated_facts:
        if f['editExpected']:
            assert f['edited']
            assert f['newValue'] == f['expectedNewValue']


@runner('simulation output variables')
def run_simulation_output_variables(model_ids: List[str],
                                    output_variables: List[str]):
    m = Modeling.simulation_output_variables(model_ids, output_variables)
    mids = set([md.id for md in m])
    assert set(model_ids) == mids
    for model in m:
        for line_item in model.line_items:
            for ov in output_variables:
                assert ov in line_item.tags


@runner('set facts tracked')
def run_set_facts_tracked():
    pass
