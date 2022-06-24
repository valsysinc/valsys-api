from dataclasses import dataclass


@dataclass
class Fact:
    uid: str
    identifier: str
    formula: str
    period: float
    value: float
    fmt: str

    @classmethod
    def from_json(cls, data):
        return cls(
            uid=data["uid"],
            identifier=data.get("identifier", ""),
            formula=data.get("formula", ""),
            period=data.get("period", 0),
            value=data.get("value", 0),
            fmt=data.get("fmt", ""),
        )
