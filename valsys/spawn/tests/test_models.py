from valsys.spawn.models import FormulaEditConfig
import pytest


class TestFormulaEditConfig:
    def test_works_ok(self):
        period_name = 'pn'
        period_year = 'py'
        formula = 'form'
        fec = FormulaEditConfig(period_name=period_name, period_year=period_year, formula=formula)
        assert fec.formula == formula
        assert fec.period_name == period_name
        assert fec.period_year == period_year

    def test_from_json(self):
        period_name = 'pn'
        period_year = 'py'
        formula = 'form'
        input_json = {
            'periodName': period_name,
            'periodYear': period_year,
            'formula': formula
        }
        fec_fk = FormulaEditConfig.from_json(input_json)
        assert fec_fk.formula == formula
        assert fec_fk.period_name == period_name
        assert fec_fk.period_year == period_year

    def test_from_json_no_formula(self):
        period_name = 'pn'
        period_year = 'py'

        input_json = {
            'periodName': period_name,
            'periodYear': period_year,
        }
        with pytest.raises(ValueError) as err:
            FormulaEditConfig.from_json(input_json)
        assert 'formula' in str(err)

    def test_from_json_no_period_year(self):
        period_name = 'pn'
        formula = 'form'

        input_json = {
            'periodName': period_name,
            'formula': formula
        }
        with pytest.raises(ValueError) as err:
            FormulaEditConfig.from_json(input_json)
        assert 'periodYear' in str(err)

    def test_from_json_no_period_year_or_formula(self):
        period_name = 'pn'

        input_json = {
            'periodName': period_name,

        }
        with pytest.raises(ValueError) as err:
            FormulaEditConfig.from_json(input_json)
        assert 'periodYear' in str(err)
        assert 'formula' in str(err)
