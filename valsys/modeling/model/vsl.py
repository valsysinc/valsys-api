
from dataclasses import dataclass, field
from typing import Dict, Any, List, Union

DEFAULT_SORT_DIRECTION = 'asc'


class WidgetTypes:
    LINE_CHART = 'LINE_CHART'
    BAR_CHART = 'BAR_CHART'
    TABLE = 'TABLE'
    DASHBOARD = 'DASHBOARD'
    WIDGET = 'WIDGET'


@dataclass
class DataPoint:
    value: str
    format: str

    class fields:
        VALUE = 'value'
        FORMAT = 'format'

    @classmethod
    def from_json(cls, j: Dict[str, Any]):
        return cls(
            value=j.get(cls.fields.VALUE),
            format=j.get(cls.fields.FORMAT)
        )


@dataclass
class VSLDataSet:
    label: str
    data: List[DataPoint] = field(default_factory=list)

    class fields:
        LABEL = 'label'
        DATA = 'data'

    @classmethod
    def from_json(cls, j: Dict[str, Any]):
        return cls(
            label=j.get(cls.fields.LABEL),
            data=[DataPoint.from_json(p) for p in j.get(cls.fields.DATA)]
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
    def from_json(cls, data: Dict[str, Any]):
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
    def from_json(cls, data: Dict[str, Any]):
        return cls(
            labels=data.get(cls.fields.LABELS),
            data_sets=[VSLDataSet.from_json(d)
                       for d in data.get(cls.fields.DATASETS)],
            opts=data.get(cls.fields.OPTS)
        )


@dataclass
class VSLSelector:
    label: str
    stype: str
    options: List[str] = field(default_factory=list)
    dependant_selectors: List[str] = field(default_factory=list)

    class fields:
        LABEL = 'label'
        OPTIONS = 'available_options'
        STYPE = 'type'
        DEPENDENT_SELECTORS = 'dependant_selectors'

    @classmethod
    def from_json(cls, j: Dict[str, Any]):
        return cls(
            label=j.get(cls.fields.LABEL),
            options=[{'label': s.get('label'), 'value': s.get(
                'value')} for s in j.get(cls.fields.OPTIONS)],
            stype=j.get(cls.fields.STYPE),
            dependant_selectors=j.get(cls.fields.DEPENDENT_SELECTORS, [])
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
        elif r.widget_type == WidgetTypes.BAR_CHART:
            r.data = VSLChartData.from_json(data.get(cls.fields.DATA))
        else:
            print(data)
            raise NotImplementedError(f"unknown widget type {r.widget_type}")
        return r


@dataclass
class VSLSelectorsResponse:
    selectors: List[VSLSelector] = field(default_factory=list)

    class fields:
        SELECTORS = 'selectors'

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        return cls(
            selectors=[VSLSelector.from_json(s)
                       for s in data.get(cls.fields.SELECTORS)]
        )
