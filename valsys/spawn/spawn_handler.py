from dataclasses import dataclass, field
from typing import Any, Dict, List

from valsys.auth import authenticate
from valsys.config import API_PASSWORD, API_USERNAME
from valsys.modeling.exceptions import ShareModelException, TagModelException
from valsys.modeling.service import share_model, spawn_model, tag_model
from valsys.seeds.models import ModelSeedConfigurationData
from valsys.spawn.exceptions import ModelSpawnException
from valsys.spawn.models import SpawnProgress, SpawnedModels


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
            self.model_id = spawn_model(config=config,
                                        auth_token=self.auth_token)
            self.progress.mark_spawned(model_id=self.model_id)
        except ModelSpawnException as err:
            self.progress.mark_spawned(err=err)

    def tag(self, tags: List[str]):
        """Tag the spawned model."""
        if self.model_id is None:
            return
        if len(tags) == 0:
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
        if len(emails) == 0:
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
        seeds: List[ModelSeedConfigurationData],
        tags: List[str] = None,
        emails: List[str] = None,
        options: Dict[str, Any] = None,
    ) -> List[SpawnProgress]:
        """Build and spawn models from the provided model configurations."""

        tags = tags or []
        emails = emails or []
        options = options or {"verbose": True}
        user, password = API_USERNAME, API_PASSWORD

        progress = []
        for config in seeds:
            auth_token = authenticate(username=user, password=password)
            handler = SpawnHandler(auth_token)
            handler.progress.ticker = config.ticker
            handler.spawn(config)
            handler.tag(tags=tags)
            handler.share(emails=emails)
            progress.append(handler.progress)
        return progress
