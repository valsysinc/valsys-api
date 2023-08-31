
from dataclasses import dataclass, field
from typing import Dict, Any, List, Union

DEFAULT_SORT_DIRECTION = 'asc'


class WidgetTypes:
    LINE_CHART = 'LINE_CHART'
    TABLE = 'TABLE'


@dataclass
class Point:
    value: str
    format: str

    class fields:
        VALUE = 'value'
        FORMAT = 'format'

    @classmethod
    def from_json(cls, j):
        return cls(
            value=j.get(cls.fields.VALUE),
            format=j.get(cls.fields.FORMAT)
        )


@dataclass
class VSLDataSet:
    label: str
    data: List[Point] = field(default_factory=list)

    class fields:
        LABEL = 'label'
        DATA = 'data'

    @classmethod
    def from_json(cls, j):
        return cls(
            label=j.get(cls.fields.LABEL),
            data=[Point.from_json(p) for p in j.get(cls.fields.DATA)]
        )


@dataclass
class VSLTableData:
    sortBy: str = ''
    sortDirection: str = ''
    rows: List[List[str]] = field(default_factory=list)
    columns: List[str] = field(default_factory=list)

    class fields:
        SORT_BY = 'sortBy'
        SORT_DIRECTION = 'sortDirection'
        ROWS = 'rows'
        COLUMNS = 'columns'

    @classmethod
    def from_json(cls, data):
        return cls(
            sortBy=data.get(cls.fields.SORT_BY),
            sortDirection=data.get(cls.fields.SORT_DIRECTION),
            columns=data.get(cls.fields.COLUMNS),
            rows=data.get(cls.fields.ROWS)
        )


@dataclass
class VSLChartData:
    labels: List[str] = field(default_factory=list)
    data_sets: List[VSLDataSet] = field(default_factory=list)
    opts: Dict[str, Any] = field(default_factory=dict)

    class fields:
        LABELS = 'labels'
        DATASETS = 'datasets'
        OPTS = 'opts'

    @classmethod
    def from_json(cls, data):
        return cls(
            labels=data.get(cls.fields.LABELS),
            data_sets=[VSLDataSet.from_json(d)
                       for d in data.get(cls.fields.DATASETS)],
            opts=data.get(cls.fields.OPTS)
        )


@dataclass
class VSLQueryResponse:
    widget_type: str
    data: Union[VSLTableData, VSLChartData] = None

    class fields:
        WIDGET_TYPE = 'widgetType'
        DATA = 'data'

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        r = cls(widget_type=data.get(cls.fields.WIDGET_TYPE))
        if r.widget_type == WidgetTypes.TABLE:
            r.data = VSLTableData.from_json(data.get(cls.fields.DATA))
        elif r.widget_type == WidgetTypes.LINE_CHART:
            r.data = VSLChartData.from_json(data.get(cls.fields.DATA))
        else:
            raise NotImplementedError(f"unknown widget type {r.widget_type}")
        return r
