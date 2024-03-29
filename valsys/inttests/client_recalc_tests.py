from valsys.inttests.runners import modeling as Runners
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
        Runners.run_recalculate_model(self.model_id, expect_facts=False)

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
                # If here, then break out the while loop:
                # something changed and we can now figure out
                # if it changed in the expected manner.
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
            'ticker': 'AAP US',
            # 'templateId': '29376a9e-a640-4b5f-a839-c355c894b740',
            'templateId': '9a514349-474f-48f3-8527-6f15ad5991c6',

            'numForecastYears': 5,
            'numHistoricalYears': 3,
            'industry': 'RETAIL-EATING \u0026 DRINKING PLACES',
            'startPeriod': 2020,
            'startDate': yesterday(),
            "variables": {
                "INTERNAL_SOURCE": "SBUX_US|respawn|ddi|amohammad"
            }
        }

    def _pull_model(self):
        return Runners.run_pull_model(self.model_id)
