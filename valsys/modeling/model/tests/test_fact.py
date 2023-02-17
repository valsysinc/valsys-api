from valsys.modeling.model.fact import Fact
import pytest


class TestFact:

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
    def test_from_json_numeric(self, numeric_format):
        uid = '1'
        valueIn, value = '42', 42

        j = {
            Fact.fields.UID: uid,
            Fact.fields.FORMAT: numeric_format,
            Fact.fields.VALUE: valueIn
        }
        fact = Fact.from_json(j)
        assert fact.value == value
        assert fact.uid == uid
        assert fact.numeric

    @pytest.mark.parametrize("valueIn,value", [('42', 42), ('', 0), (' ', 0),
                                               (' ' * 10, 0)])
    def test_from_json_numeric_valid_values(self, valueIn, value):
        uid = '1'

        j = {
            Fact.fields.UID: uid,
            Fact.fields.FORMAT: 'numeric',
            Fact.fields.VALUE: valueIn
        }
        fact = Fact.from_json(j)
        assert fact.value == value
        assert fact.uid == uid
        assert fact.numeric

    @pytest.mark.parametrize("non_numeric_format",
                             ['blah', "{'valFormat':'val'}"])
    def test_from_json_not_numeric(self, non_numeric_format):
        uid = '1'
        value = '42'

        j = {
            Fact.fields.UID: uid,
            Fact.fields.FORMAT: non_numeric_format,
            Fact.fields.VALUE: value
        }
        fact = Fact.from_json(j)
        assert fact.value == value
        assert fact.uid == uid
        assert not fact.numeric