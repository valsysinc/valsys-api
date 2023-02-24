import pytest

from valsys.modeling.model.fact import Fact


class TestFact:

    def json(self, uid, fmt, json_value):
        return {
            Fact.fields.UID: uid,
            Fact.fields.FORMAT: fmt,
            Fact.fields.VALUE: json_value
        }

    def fact_from_json(self, uid, format_str, json_value):
        j = self.json(uid, format_str, json_value)
        return Fact.from_json(j)

    def test_init(self):
        uid = '1'
        identifier = '2'
        formula = "f"
        period = 2019
        value = '42'
        fmt = '{}'
        numeric = True
        fact = Fact(uid=uid,
                    identifier=identifier,
                    formula=formula,
                    period=period,
                    value=value,
                    fmt=fmt,
                    numeric=numeric)
        assert fact.numeric

    @pytest.mark.parametrize("numeric_format", [
        'numeric', 'Numeric', "{'valFormat':'numeric'}",
        "{'valFormat':'1numeric'}"
    ])
    def test_from_json_valid_numeric_formats(self, numeric_format):
        uid, json_value, value = '1', '42', 42
        fact = self.fact_from_json(uid=uid,
                                   format_str=numeric_format,
                                   json_value=json_value)
        assert fact.value == value
        assert fact.uid == uid
        assert fact.numeric

    @pytest.mark.parametrize("json_value,value", [('42', 42), ('', 0),
                                                  (' ', 0), (' ' * 10, 0)])
    def test_from_json_numeric_valid_values(self, json_value, value):
        uid, format_str = '1', 'numeric'
        fact = self.fact_from_json(uid, format_str, json_value)
        assert fact.value == value
        assert fact.uid == uid
        assert fact.numeric

    @pytest.mark.parametrize("non_numeric_format",
                             ['blah', "{'valFormat':'val'}"])
    def test_from_json_not_numeric_format(self, non_numeric_format):
        uid, value = '1', '42'
        fact = self.fact_from_json(uid, non_numeric_format, value)
        assert fact.value == value
        assert fact.uid == uid
        assert not fact.numeric
