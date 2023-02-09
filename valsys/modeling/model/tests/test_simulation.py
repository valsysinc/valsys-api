from valsys.modeling.model.simulation import SimulationResponse
from valsys.modeling.model.tests.fixtures import sample_simulation_response


class TestSimulationResponse:

    def test_works_ok_from_json(self):
        resp = sample_simulation_response()
        s = SimulationResponse.from_json(resp)
        assert len(s.simulation.simulations) == 2
        assert len(s.group_data.models) == 2
        model_0_fields = [f.field for f in s.group_data.models[0].fields]
        assert set(model_0_fields) == set([
            'Change in IRR', 'Current share price (DCF)',
            'Implied premium (DCF)', 'Implied share price (DCF)',
            'Perpetual growth rate (DCF)',
            'Perpetual growth rate (DCF) (Simulated)', 'Ticker'
        ])
