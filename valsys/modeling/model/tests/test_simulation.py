from valsys.modeling.model.simulation import SimulationResponse, Edit
from valsys.modeling.model.tests.fixtures import sample_simulation_response

import pytest


class TestSimulationResponse:

    def test_works_ok_from_json(self):
        resp = sample_simulation_response()
        s = SimulationResponse.from_json(resp)
        assert len(s.simulation) == 2
        assert len(s.group_data) == 2
        model_0_fields = [f.field for f in s.group_data[0].group_fields]
        assert set(model_0_fields) == set([
            'Change in IRR', 'Current share price (DCF)',
            'Implied premium (DCF)', 'Implied share price (DCF)',
            'Perpetual growth rate (DCF)',
            'Perpetual growth rate (DCF) (Simulated)', 'Ticker'
        ])


class TestEdit:

    @pytest.mark.parametrize('edit', [{
        'formula': '$FORMULA + 1',
        'timePeriod': "LFY+1"
    }, {
        'formula': '$FORMULA * 1',
        'timePeriod': "LFY-1"
    }])
    def test_validate_ok(self, edit):
        assert Edit.validate(edit)

    @pytest.mark.parametrize('edit', [{
        '1formula': '',
        '1timePeriod': ""
    }, {
        'formula': '',
        '1timePeriod': ""
    }, {
        '1formula': '',
        'timePeriod': ""
    }])
    def test_validate_invalid_keys(self, edit):
        with pytest.raises(AssertionError):
            Edit.validate(edit)

    @pytest.mark.parametrize('edit', [{'formula': 'FORMULA + 1'}])
    def test_validate_fail_formula(self, edit):
        with pytest.raises(AssertionError):
            Edit.validate(edit)

    @pytest.mark.parametrize('edit', [{
        'formula': '$FORMULA + 1',
        'timePeriod': '74893'
    }])
    def test_validate_fail_time_period(self, edit):
        with pytest.raises(AssertionError):
            Edit.validate(edit)
