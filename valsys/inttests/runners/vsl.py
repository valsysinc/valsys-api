

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


from valsys.inttests.runners.vsl_utils import pluck_tags, wait_check_facts_tracked, wait_check_formula_edited


@dataclass
class VSLRunProps:
    model_id_1: str
    model_id_2: str
    tag: str
    nedits: int


def run_vsl_tests(model_id_1: str, model_id_2: str):
    '''
    setup_and_run_vsl will setup the nessecary models and edits
    for testing the VSL, and then will execute the VSL tests.
    '''
    model = Runners.run_pull_model(model_id_1)
    case_id, line_item = pluck_tags(model)
    fact_to_edit = line_item.facts[0]
    Runners.run_set_facts_tracked([model_id_1], line_item.tags)
    wait_check_facts_tracked(model_id_1, line_item.uid)

    formulae_edits = ['42', '84', '168']

    for formula_edit in formulae_edits:
        Runners.run_edit_formula(
            model_id_1, case_id, fact=fact_to_edit, new_formula=formula_edit)
        wait_check_formula_edited(model_id_1, line_item.uid,
                                  fact_to_edit.uid, formula_edit)

    props = VSLRunProps(
        model_id_1=model_id_1,
        model_id_2=model_id_2,
        tag=line_item.tags[0],
        nedits=len(formulae_edits)
    )

    # Now run the various VSL-type tests.
    run_garbage(props.model_id_1)
    run_simple_filter(props.model_id_1, tag=props.tag)
    run_multi_column([props.model_id_1, props.model_id_2], tag=props.tag)

    run_multi_column_var_model_ids(
        [props.model_id_1, props.model_id_2], tag=props.tag)
    run_multi_column_with_funcs(
        [props.model_id_1, props.model_id_2], tag=props.tag)
    #run_history(props.model_id_1, tag=props.tag, nedits=props.nedits)
    run_history_multiple_traces(
        props.model_id_1, tag=props.tag, nedits=props.nedits)
    run_using_histories(props.tag)
    run_simple_selector()
    run_chaining_selectors()
    run_dashboard_selector()
    run_dashboard_widget_selector()
    run_filter_to_line_charts(props.tag)
    run_filter_to_bar_charts(props.model_id_1, tag=props.tag)
    run_selector_with_line_item_tags()


@runner('garbage queries that should fail')
def run_garbage(model_id: str):
    column_label = "Some column for revenue"
    queries = ['''filter().Table()''', f'''
    Filter(modelID=\"{model_id}\").
    Columns(label=\"{column_label}\", tag=[Total Revenue (Revenue)[LFY]]).
    Table()''']
    for query in queries:
        try:
            vsl.execute_vsl_query(query)
        except ModelingServicePostException:
            continue
        raise AssertionError(f"expected error for query {query}")


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


@runner('multi column filter with funcs')
def run_multi_column_with_funcs(model_ids: List[str], tag='Total Revenue (Revenue)'):

    model_ids_str = modelids_to_csv(model_ids, "[", "]")
    func_names = ['doubleIt', 'multiplyBy2']
    for func_name in func_names:
        query = f'''
        var { func_name } = func(x) {{ x * 2 }};

        Filter(modelID={model_ids_str}).
        Column(label="Revenue", field="ticker").
        Column(label="labelModelID", field="modelID").
        Column(label="Expression label", expression=([{tag}[LFY]] / { func_name }([{tag}[LFY-1]]))).
        Table()
        '''

        r = vsl.execute_vsl_query(query)
        assert_equal(r.widget_type, WidgetTypes.TABLE)
        assert_equal(r.data.sortBy, 'Revenue')
        assert_equal(len(r.data.columns), 3)
        assert_equal(len(r.data.rows), 2)
        assert_equal(
            set(['Revenue', 'labelModelID', 'Expression label']), set(r.data.columns))


@runner('multi column filter with var modelids')
def run_multi_column_var_model_ids(model_ids: List[str], tag):
    model_ids_str = modelids_to_csv(model_ids, "[", "]")

    query = '''
    var mids = '''+model_ids_str+''';
    
    Filter(modelID=mids).
    Column(label="Revenue", field="ticker").
    Column(label="labelModelID", field="modelID").
    Column(label="Expression label", expression=([''' + tag + '''[LFY]] / 1.1*[''' + tag + '''[LFY-1]])).
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


@runner('simple single selector')
def run_simple_selector():
    query = f'''
    var analyst = Selector(label="Analyst", source="models", field="created_by");

    ReturnAllSelectors();
    '''
    r = vsl.execute_vsl_query_selectors(query)
    assert_equal(len(r.selectors), 1, 'number of selectors')
    assert_equal(r.selectors[0].stype, WidgetTypes.WIDGET, 'selector type')
    assert_equal(len(r.selectors[0].dependant_selectors),
                 0, 'number of dependent selectors')


@runner('chaining selectors')
def run_chaining_selectors():
    query = f'''
    var title = Selector(label="Title", source="models", field="title");
    var ticker = Selector(label="Ticker", source="models", field="ticker", given=title);
    var analyst = Selector(label="Analyst", source="models", field="created_by", given=ticker);

    ReturnAllSelectors(title, ticker, analyst)
    '''
    r = vsl.execute_vsl_query_selectors(query)

    assert set(["Title", "Ticker", "Analyst"]) == set(
        [s.label for s in r.selectors])

    assert_equal(len(r.selectors), 3, 'number of selectors')
    assert_equal(r.selectors[0].stype, WidgetTypes.WIDGET, 'selector type')
    assert_equal(len(r.selectors[0].dependant_selectors),
                 2, 'number of dependent selectors')
    assert_equal(len(r.selectors[1].dependant_selectors),
                 1, 'number of dependent selectors')
    assert_equal(len(r.selectors[2].dependant_selectors),
                 0, 'number of dependent selectors')


@runner('dashboard selector')
def run_dashboard_selector():
    query = '''
    var ticker = Selector(label="Ticker", source="models", field="ticker", dashboardSelector=TRUE, widgetSelector=FALSE)
    ReturnAllSelectors(ticker)
    '''
    r = vsl.execute_vsl_query_selectors(query)
    assert_equal(len(r.selectors), 1)
    assert_equal(r.selectors[0].stype, WidgetTypes.DASHBOARD, 'selector type')


@runner('dashboard and widget selector')
def run_dashboard_widget_selector():
    query = '''
    var ticker = Selector(label="Ticker", source="models", field="ticker", dashboardSelector=TRUE, widgetSelector=TRUE)
    ReturnAllSelectors(ticker)
    '''
    r = vsl.execute_vsl_query_selectors(query)

    assert set([WidgetTypes.DASHBOARD, WidgetTypes.WIDGET]) == set(
        [s.stype for s in r.selectors])

    assert_equal(len(r.selectors), 2)


@runner('history to line chart')
def run_history_to_line_chart(model_id, tag='Revenue (Base)', nedits=0):
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


@runner('using histories')
def run_using_histories(tag):
    query = f'''
    Filter().
	Histories(modelFieldLabel="ticker", tag=[{tag}[LFY]], stepped="middle").
	LineChart()
    '''
    r = vsl.execute_vsl_query(query)
    assert_equal(r.widget_type, WidgetTypes.LINE_CHART)


@runner('filter to line charts')
def run_filter_to_line_charts(tag):
    queries = [
        f'''
    Filter().
	Series(modelFieldLabel="ticker", lineItem="{tag}").
	LineChart()
    ''',
        f'''
    Filter().
	Series(modelFieldLabel="ticker", lineItem="{tag}").
	LineChart(start="LFY", end="LFY+2")
    '''
    ]
    for query in queries:
        r = vsl.execute_vsl_query(query)
        assert_equal(r.widget_type, WidgetTypes.LINE_CHART, 'widget type')


@runner('filter to bar charts')
def run_filter_to_bar_charts(model_id: str, tag: str):
    queries = [
        f'''
    Filter(modelID=\"{model_id}\").
	Series(modelFieldLabel="ticker", lineItem="{tag}").
	BarChart()
    ''',
        f'''
    Filter().
	Series(modelFieldLabel="ticker", lineItem="{tag}").
	BarChart()
    ''',
        f'''
    Filter(modelID=\"{model_id}\").
	Series(modelFieldLabel="ticker", lineItem="{tag}").
	BarChart(start="LFY", end="LFY+2")
    '''
    ]
    for query in queries:
        r = vsl.execute_vsl_query(query)
        assert_equal(r.widget_type,  WidgetTypes.BAR_CHART, 'widget type')


@runner('run_selector_with_line_item_tags')
def run_selector_with_line_item_tags():
    query = f'''
    var lineItem = Selector(label="Tag", source="line_items", field="tag")

    ReturnAllSelectors(lineItem)
    '''
    r = vsl.execute_vsl_query_selectors(query)
    assert_equal(len(r.selectors), 1, 'number of selectors')
    assert_equal(r.selectors[0].stype, WidgetTypes.WIDGET, 'selector type')
