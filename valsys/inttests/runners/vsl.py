import time

from dataclasses import dataclass
from typing import List
from valsys.inttests.runners.utils import (
    assert_equal,
    assert_true,
    assert_gt,
    assert_contains,
    runner,
    modelids_to_csv
)
from valsys.modeling import vsl as vsl
from valsys.modeling.model.vsl import DEFAULT_SORT_DIRECTION, WidgetTypes
from valsys.modeling.client.exceptions import ModelingServicePostException
from valsys.inttests.runners import modeling as Runners
from valsys.modeling.model.model import Model


@dataclass
class VSLRunProps:
    model_id_1: str
    model_id_2: str
    tag: str
    nedits: int


def pluck_tags(model: Model):
    for c in model.cases:
        for m in c.modules:
            for l in m.line_items:
                if l.tags != []:
                    for f in l.facts:
                        if f.value != '':
                            return c.uid, l
    raise Exception('cannot find line item with tags')


def setup_and_run_vsl(model_id_1, model_id_2):
    model = Runners.run_pull_model(model_id_1)

    caseid, line_item_with_tags = pluck_tags(model)

    Runners.run_set_facts_tracked([model_id_1], line_item_with_tags.tags)
    model_id_2 = Runners.run_copy_model(model_id_1)
    time.sleep(10)
    model_repulled = Runners.run_pull_model(model_id_1)
    lip = model_repulled.pull_line_item(line_item_with_tags.uid)
    time.sleep(10)
    Runners.run_edit_formula(
        model_id_1, caseid, fact=lip.facts[0], new_formula="42")
    time.sleep(10)
    Runners.run_edit_formula(
        model_id_1, caseid, fact=lip.facts[0], new_formula="84")
    time.sleep(10)
    Runners.run_edit_formula(
        model_id_1, caseid, fact=lip.facts[0], new_formula="168")
    time.sleep(10)

    run_vsl(VSLRunProps(
        model_id_1=model_id_1,
        model_id_2=model_id_2,
        tag=lip.tags[0],
        nedits=3
    ))


def run_vsl(props: VSLRunProps):
    '''This func will run the various VSL-type tests.'''
    run_garbage(props.model_id_1)
    run_simple_filter(props.model_id_1, tag=props.tag)
    run_multi_column([props.model_id_1, props.model_id_2], tag=props.tag)
    #run_multi_column_func([model_id_1, model_id_2])
    #run_multi_column_var_model_ids([model_id_1, model_id_2])
    #run_multi_column_func2([model_id_1, model_id_2])
    run_history(props.model_id_1, tag=props.tag, nedits=props.nedits)
    run_history_multiple_traces(
        props.model_id_1, tag=props.tag, nedits=props.nedits)


@runner('garbage query')
def run_garbage(model_id: str):
    column_label = "Some column for revenue"
    query = f'''
    Filter(modelID=\"{model_id}\").
    Columns(label=\"{column_label}\", tag=[Total Revenue (Revenue)[LFY]]).
    Table()'''
    try:
        vsl.execute_vsl_query(query)
    except ModelingServicePostException as err:
        return
    raise AssertionError("expected to get an error and didnt")


@runner('simple filter')
def run_simple_filter(model_id: str, tag='Total Revenue (Revenue)'):
    column_label = "Some column for revenue"
    query = f'''
    Filter(modelID=\"{model_id}\").
    Column(label=\"{column_label}\", tag=[{tag}[LFY]]).
    Table()'''
    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, WidgetTypes.TABLE)
    assert_contains(r.data.columns, [column_label])
    assert_equal(r.data.sortBy, column_label)
    assert_equal(r.data.sortDirection, DEFAULT_SORT_DIRECTION)
    assert_equal(len(r.data.rows), 1)
    assert_equal(len(r.data.columns), 1)


@runner('multi column filter')
def run_multi_column(model_ids: List[str], tag='Total Revenue (Revenue)'):

    model_ids_str = modelids_to_csv(model_ids, "[", "]")

    query = f'''
    Filter(modelID={model_ids_str}).
    Column(label="Revenue", field="ticker").
    Column(label="labelModelID", field="modelID").
    Column(label="Expression label", expression=([{tag}[LFY]] / 1.1*[{tag}[LFY-1]])).
    Table()
    '''
    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, WidgetTypes.TABLE)
    assert_equal(r.data.sortBy, 'Revenue')
    assert_equal(r.data.sortDirection, DEFAULT_SORT_DIRECTION)
    assert_equal(len(r.data.columns), 3)
    assert_equal(len(r.data.rows), 2)
    mids_in_rows = set(rw[1] for rw in r.data.rows)
    assert mids_in_rows == set(model_ids)


@runner('multi column filter with func')
def run_multi_column_func(model_ids: List[str]):

    model_ids_str = modelids_to_csv(model_ids, "[", "]")

    query = '''
    var doubleIt = func(x) { x * 2 };

    Filter(modelID='''+model_ids_str+''').
    Column(label="Revenue", field="ticker").
    Column(label="labelModelID", field="modelID").
    Column(label="Expression label", expression=([Total Revenue (Revenue)[LFY]] / doubleIt([Total Revenue (Revenue)[LFY-1]]))).
    Table()
    '''

    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, WidgetTypes.TABLE)
    assert_equal(r.data.sortBy, 'Revenue')
    assert_equal(r.data.sortDirection, DEFAULT_SORT_DIRECTION)
    assert_equal(len(r.data.columns), 3)
    assert_equal(len(r.data.rows), 2)


@runner('multi column filter with func with number')
def run_multi_column_func2(model_ids: List[str]):

    model_ids_str = modelids_to_csv(model_ids, "[", "]")

    query = '''
    var multiplyBy2 = func(x) { x * 2 };

    Filter(modelID='''+model_ids_str+''').
    Column(label="Revenue", field="ticker").
    Column(label="labelModelID", field="modelID").
    Column(label="Expression label", expression=([Total Revenue (Revenue)[LFY]] / multiplyBy2([Total Revenue (Revenue)[LFY-1]]))).
    Table()
    '''

    r = vsl.execute_vsl_query(query)
    print(r)


@runner('multi column filter with var modelids')
def run_multi_column_var_model_ids(model_ids: List[str]):
    model_ids_str = modelids_to_csv(model_ids, "[", "]")

    query = '''
    var mids = '''+model_ids_str+''';
    
    Filter(modelID=mids).
    Column(label="Revenue", field="ticker").
    Column(label="labelModelID", field="modelID").
    Column(label="Expression label", expression=([Total Revenue (Revenue)[LFY]] / 1.1*[Total Revenue (Revenue)[LFY-1]])).
    Table()
    '''

    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, WidgetTypes.TABLE)
    assert_equal(r.data.sortBy, 'Revenue')
    assert_equal(r.data.sortDirection, DEFAULT_SORT_DIRECTION)
    assert_equal(len(r.data.columns), 3)
    assert_equal(len(r.data.rows), 2)
    mids_in_rows = set(rw[1] for rw in r.data.rows)
    assert mids_in_rows == set(model_ids)


@runner('history')
def run_history(model_id, tag='Revenue (Base)', nedits=0):
    query = f'''
    Filter(modelID=\"{model_id}\").
    History(label="Base", tag=[{tag}[LFY-1]]).
    LineChart()'''
    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, WidgetTypes.LINE_CHART)
    assert_gt(len(r.data.labels), 0, 'number of data labels')
    assert_equal(len(r.data.data_sets), 1, 'number of data sets')
    assert_true(r.data.opts['time'], 'time is an option')


@runner('history multiple traces')
def run_history_multiple_traces(model_id, tag='Revenue (Base)', nedits=0):
    query = f'''
    Filter(modelID=\"{model_id}\").
    History(label="Base1", tag=[{tag}[LFY-1]]).
    History(label="Base2", tag=[{tag}[LFY-1]]).
    LineChart()'''
    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, WidgetTypes.LINE_CHART)
    assert_gt(len(r.data.labels), 0, 'number of data labels')
    assert_equal(len(r.data.data_sets), 2, 'number of data sets')
    assert_true(r.data.opts['time'], 'time is an option')
