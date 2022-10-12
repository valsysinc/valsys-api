from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class DependentFact:
    uid: str
    identifier: str
    period: float

    def jsonify(self):
        return {
            'id': self.uid,
            'identifier': self.identifier,
            'period': self.period
        }

    @classmethod
    def from_json(cls, j):
        return cls(uid=j.get('id'),
                   identifier=j.get('identifier'),
                   period=j.get('period'))


@dataclass
class PrecedentFact:
    uid: str
    identifier: str
    period: float

    def jsonify(self):
        return {
            'id': self.uid,
            'identifier': self.identifier,
            'period': self.period
        }

    @classmethod
    def from_json(cls, j):
        return cls(uid=j.get('id'),
                   identifier=j.get('identifier'),
                   period=j.get('period'))


@dataclass
class Fact:
    uid: str
    identifier: str
    formula: str
    internal_formula: str
    period: float
    data_value: str
    value: float
    fmt: str
    note: str
    date_format: str
    dep_cells: List[Any] = field(default_factory=list)
    pre_cells: List[Any] = field(default_factory=list)

    class fields:
        UID = 'id'
        DATE_FORMAT = 'dateFormat'
        FORMULA = 'formula'
        INTERNAL_FORMULA = 'internalFormula'
        PERIOD = 'period'
        IDENTIFIER = 'identifier'
        FMT = 'fmt'
        VALUE = 'value'
        DATA_VALUE = 'dataValue'
        FORMAT = 'format'
        EDGES = 'edges'
        NOTE = 'note'
        DEP_CELLS = 'dependantCells'
        PRE_CELLS = 'precedentCells'

    def jsonify(self, fields: Optional[List[str]] = None):
        all_fields = {
            self.fields.UID: self.uid,
            self.fields.FORMULA: self.formula,
            self.fields.INTERNAL_FORMULA: self.internal_formula,
            self.fields.DATE_FORMAT: self.date_format,
            self.fields.PERIOD: self.period,
            self.fields.IDENTIFIER: self.identifier,
            self.fields.DATA_VALUE: self.data_value,
            self.fields.FMT: self.fmt,
            self.fields.NOTE: self.note,
            self.fields.FORMAT: self.fmt,
            self.fields.EDGES: {
                self.fields.DEP_CELLS: [dc.jsonify() for dc in self.dep_cells],
                self.fields.PRE_CELLS: [pc.jsonify() for pc in self.pre_cells]
            }
        }
        if fields is None:
            return all_fields
        else:
            return {f: all_fields[f] for f in fields}

    @classmethod
    def from_json(cls, data):
        return cls(
            uid=data[cls.fields.UID],
            identifier=data.get(cls.fields.IDENTIFIER, ""),
            date_format=data.get(cls.fields.DATE_FORMAT, ""),
            formula=data.get(cls.fields.FORMULA, ""),
            internal_formula=data.get(cls.fields.INTERNAL_FORMULA, ""),
            period=data.get(cls.fields.PERIOD, 0),
            value=data.get(cls.fields.VALUE, 0),
            data_value=data.get(cls.fields.DATA_VALUE, ""),
            fmt=data.get(cls.fields.FMT, ""),
            note=data.get(cls.fields.NOTE, ""),
            dep_cells=[
                DependentFact.from_json(f)
                for f in data.get('edges', {}).get(cls.fields.DEP_CELLS, [])
            ],
            pre_cells=[
                PrecedentFact.from_json(f)
                for f in data.get('edges', {}).get(cls.fields.PRE_CELLS, [])
            ])
