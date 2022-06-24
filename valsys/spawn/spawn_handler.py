from dataclasses import field, dataclass
from typing import List
from tqdm import tqdm
import pyfiglet
from valsys.utils import logger
from valsys.spawn.models import ModelSeedConfigurationData, SpawnProgress
from valsys.spawn.exceptions import ModelSpawnException
from valsys.modeling.exceptions import TagModelException, ShareModelException
from valsys.modeling.service import tag_model, share_model, spawn_model
from valsys.version import VERSION, NAME
from valsys.auth import authenticate
from valsys.config import API_PASSWORD, API_USERNAME


@dataclass
class SpawnHandler:
    """The `SpawnHandler` class handles everything to do with
    model spawning and subsequent interactions.

    At any point, one can interrogate the `progress` atrribute
    to find out which subprocess of the spawning has taken place,
    and if there are any errors.
    """

    auth_token: str
    progress: SpawnProgress = field(default_factory=SpawnProgress)
    model_id: str = None

    def spawn(self, config: ModelSeedConfigurationData):
        """Use the provided configuration to spawn a model."""
        try:
            self.model_id = spawn_model(config=config, auth_token=self.auth_token)
            self.progress.mark_spawned(model_id=self.model_id)
        except ModelSpawnException as err:
            self.progress.mark_spawned(err=err)

    def tag(self, tags: List[str]):
        """Tag the spawned model."""
        if self.model_id is None:
            return
        try:
            tag_model(self.model_id, tags, self.auth_token)
            self.progress.mark_tagged()
        except TagModelException as err:
            self.progress.mark_tagged(err=err)

    def share(self, emails: List[str], permission="view"):
        """Share the spawned model with users emails.

        All users will be given the same permissions."""
        if self.model_id is None:
            return
        for email in emails:
            try:
                share_model(
                    model_id=self.model_id,
                    email=email,
                    permission=permission,
                    auth_token=self.auth_token,
                )
                self.progress.mark_shared(email, permission)
            except ShareModelException as err:
                self.progress.mark_shared(email, permission, err=err)

    @classmethod
    def build_and_spawn_models(
        cls,
        configs: List[ModelSeedConfigurationData],
        tags: List[str],
        emails: List[str],
    ) -> List[SpawnProgress]:
        """Build and spawn models from the provided model configurations."""
        print(pyfiglet.figlet_format(NAME), f"{' '*10} v{VERSION}")

        user, password = API_PASSWORD, API_USERNAME

        progress: List[SpawnProgress] = []
        for config in tqdm(configs):
            auth_token = authenticate(username=user, password=password)
            handler = SpawnHandler(auth_token)
            handler.progress.ticker = config.ticker
            handler.spawn(config)
            handler.tag(tags=tags)
            handler.share(emails=emails)
            progress.append(handler.progress)
        return progress
