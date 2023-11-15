from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Fact:
    uid: str
    identifier: str
    formula: str
    period: float
    value: str
    fmt: str
    numeric: bool

    class fields:
        UID = 'id'
        FORMULA = 'formula'
        PERIOD = 'period'
        IDENTIFIER = 'identifier'
        FMT = 'fmt'
        VALUE = 'value'
        FORMAT = 'format'

    def jsonify(self, fields: Optional[List[str]] = None):
        all_fields = {
            self.fields.UID: self.uid,
            self.fields.FORMULA: self.formula,
            self.fields.PERIOD: self.period,
            self.fields.IDENTIFIER: self.identifier,
            self.fields.FMT: self.fmt,
            self.fields.FORMAT: self.fmt
        }
        if fields is None:
            return all_fields
        else:
            return {f: all_fields[f] for f in fields}

    @classmethod
    def from_json(cls, data: Dict[str, str]):
        fmt = data.get(cls.fields.FORMAT, "")
        value = data.get(cls.fields.VALUE, "").strip()

        is_numeric = 'numeric' in fmt.lower()
        if is_numeric and value == '' or value == '-':
            value = 0
        elif is_numeric and value == '-':
            is_numeric=False
        elif is_numeric and value != '':
            value = float(value)

        return cls(uid=data[cls.fields.UID],
                   identifier=data.get(cls.fields.IDENTIFIER, ""),
                   formula=data.get(cls.fields.FORMULA, ""),
                   period=data.get(cls.fields.PERIOD, 0),
                   value=value,
                   fmt=fmt,
                   numeric=is_numeric)
