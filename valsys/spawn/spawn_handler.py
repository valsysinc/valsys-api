from dataclasses import dataclass, field
from typing import Any, Dict, List

from valsys.auth.service import authenticate
from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.modeling.exceptions import ShareModelException, TagModelException
from valsys.modeling.service import share_model, tag_model, spawn_model, SpawnedModelInfo

from valsys.spawn.exceptions import ModelSpawnException
from valsys.spawn.models import SpawnProgress
from valsys.seeds.models import OrchestratorConfig


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
        seeds: List[SpawnedModelInfo],
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
            handler.model_id = config.model_id
            handler.progress.mark_spawned(model_id=config.model_id)
            handler.progress.ticker = config.ticker
            handler.tag(tags=tags)
            handler.share(emails=emails)

            progress.append(handler.progress)

        return progress

    @classmethod
    def orchestrate_model_spawns(
        cls,
        seeds: OrchestratorConfig,
    ):
        seeds.username, seeds.password = API_USERNAME, API_PASSWORD

        models = spawn_model(seeds)
        return cls.build_and_spawn_models(models,
                                          tags=seeds.tags,
                                          emails=seeds.emails)
