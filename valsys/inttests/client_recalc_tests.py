from valsys.inttests.runners import runners as Runners
from valsys.inttests.runners.utils import assert_equal, assert_gt
from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.inttests.utils import gen_orch_config, workflow
from valsys.utils.time import yesterday
import time


class ClientRecalcTest:

    @workflow('client recalc setup')
    def setup(self):

        user, password = API_USERNAME, API_PASSWORD

        # Define the model seed configuration data
        model_seed_config = gen_orch_config(self._model_config(), user,
                                            password)

        # Spawn the model and obtain the modelID
        self.model_id = Runners.run_spawn_single_model(model_seed_config)
        self.init_model = self._pull_model()
        Runners.run_recalculate_model(self.model_id)

    @workflow('client recalc assertions')
    def post_assertions(self):

        init_periods = self.init_model.first_case.first_module.periods
        ntries = 1
        maxntries = 5
        sleep_time_secs = 20
        while True:
            model2 = self._pull_model()
            post_periods = model2.first_case.first_module.periods
            if len(post_periods) != len(init_periods):
                break
            if ntries > maxntries:
                break
            ntries += 1
            time.sleep(sleep_time_secs)
            sleep_time_secs *= 1.5

        assert_gt(len(post_periods), len(init_periods),
                  'number of periods incremented')
        assert_equal(max(post_periods),
                     max(init_periods) + 1, 'max period incremented by 1')

    @workflow('client recalc cleanup')
    def cleanup(self):
        Runners.run_delete_models([self.model_id])

    def _model_config(self):
        return {
            'companyName': 'Starbucks',
            'ticker': 'SBUX',
            'templateName': 'cpp-template',
            'numForecastYears': 5,
            'numHistoricalYears': 3,
            'industry': 'RETAIL-EATING \u0026 DRINKING PLACES',
            'startPeriod': 2018,
            'startDate': yesterday(),
            "variables": {
                "INTERNAL_SOURCE": "SBUX_US|respawn|ddi|amohammad"
            }
        }

    def _pull_model(self):
        return Runners.run_pull_model(self.model_id)
