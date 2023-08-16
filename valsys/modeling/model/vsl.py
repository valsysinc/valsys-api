
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class VSLData:
    sortBy: str
    sortDirection: str
    rows: List[List[str]]
    columns: List[str]

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
class VSLQueryResponse:
    widget_type: str
    data: VSLData = field(default_factory=VSLData)

    class fields:
        WIDGET_TYPE = 'widgetType'
        DATA = 'data'

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        return cls(
            widget_type=data.get(cls.fields.WIDGET_TYPE),
            data=VSLData.from_json(data.get(cls.fields.DATA))
        )
