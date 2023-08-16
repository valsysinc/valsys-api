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
from valsys.inttests.runners.runners import run_delete_models


@runner('simple filter')
def run_vsl_simple_filter(model_id):
    column_label = "Some column for revenue"
    query = f'Filter(modelID=\"{model_id}\").Column(label=\"{column_label}\", tag=[Total Revenue (Revenue)[LFY]]).Table()'
    r = Modeling.execute_vsl_query(query)
    print(r)
    assert_equal(r.widget_type, 'TABLE')
    assert_contains(r.data.columns, [column_label])
    run_delete_models([model_id])
