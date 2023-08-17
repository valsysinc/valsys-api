from typing import List
from valsys.inttests.runners.utils import (
    assert_equal,
    assert_contains,
    runner,
    modelids_to_csv
)
from valsys.modeling import vsl as vsl
from valsys.modeling.model.vsl import DEFAULT_SORT_DIRECTION
from valsys.modeling.client.exceptions import ModelingServicePostException


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
def run_simple_filter(model_id: str):
    column_label = "Some column for revenue"
    query = f'''
    Filter(modelID=\"{model_id}\").
    Column(label=\"{column_label}\", tag=[Total Revenue (Revenue)[LFY]]).
    Table()'''
    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, 'TABLE')
    assert_contains(r.data.columns, [column_label])
    assert_equal(r.data.sortBy, column_label)
    assert_equal(r.data.sortDirection, DEFAULT_SORT_DIRECTION)
    assert_equal(len(r.data.rows), 1)
    assert_equal(len(r.data.columns), 1)


@runner('multi column filter')
def run_multi_column(model_ids: List[str]):

    model_ids_str = modelids_to_csv(model_ids, "[", "]")

    query = '''Filter(modelID='''+model_ids_str+''').
    Column(label="Revenue", field="ticker").
    Column(label="labelModelID", field="modelID").
    Column(label="Expression label", expression=([Total Revenue (Revenue)[LFY]] / 1.1*[Total Revenue (Revenue)[LFY-1]])).
    Table()
    '''
    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, 'TABLE')
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
    assert_equal(r.widget_type, 'TABLE')
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
    print(query)
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
    print(query)
    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, 'TABLE')
    assert_equal(r.data.sortBy, 'Revenue')
    assert_equal(r.data.sortDirection, DEFAULT_SORT_DIRECTION)
    assert_equal(len(r.data.columns), 3)
    assert_equal(len(r.data.rows), 2)
    mids_in_rows = set(rw[1] for rw in r.data.rows)
    assert mids_in_rows == set(model_ids)
