from valsys.inttests.runners.utils import (
    assert_equal,
    assert_contains,
    runner,
)
from valsys.modeling import service as Modeling
from valsys.modeling.model.vsl import DEFAULT_SORT_DIRECTION


@runner('simple filter')
def run_vsl_simple_filter(model_id):
    column_label = "Some column for revenue"
    query = f'Filter(modelID=\"{model_id}\").Column(label=\"{column_label}\", tag=[Total Revenue (Revenue)[LFY]]).Table()'
    r = Modeling.execute_vsl_query(query)
    assert_equal(r.widget_type, 'TABLE')
    assert_contains(r.data.columns, [column_label])
    assert_equal(r.data.sortBy, column_label)
    assert_equal(r.data.sortDirection, DEFAULT_SORT_DIRECTION)
    assert_equal(len(r.data.rows), 1)
    assert_equal(len(r.data.columns), 1)
