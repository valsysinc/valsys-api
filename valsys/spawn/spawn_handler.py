from dataclasses import dataclass, field
from datetime import datetime
from random import seed
from typing import List

from valsys.auth.service import authenticate
from valsys.config.config import API_PASSWORD, API_USERNAME
from valsys.modeling.exceptions import ShareModelException, TagModelException
from valsys.modeling.service import (
    SpawnedModelInfo,
    share_model,
    spawn_model,
    tag_model,
)
from valsys.seeds.models import OrchestratorConfig
from valsys.spawn.models import SpawnProgress
from valsys.utils import logger


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
    def orchestrate_model_spawns(cls,
                                 seeds: OrchestratorConfig,
                                 options=None) -> List[SpawnProgress]:
        """Build and spawn models from the provided model configurations.
        
        This will put on the username and password.
        """
        seeds.username, seeds.password = API_USERNAME, API_PASSWORD
        nmodels = seeds.count_tickers
        t1 = datetime.now()
        models = spawn_model(seeds)
        t2 = datetime.now()
        logger.info(
            f"spawned {nmodels} models in {(t2-t1).total_seconds():.1f}s")

        options = options or {"verbose": True}
        user, password = API_USERNAME, API_PASSWORD

        progress = []
        tags, emails = seeds.tags, seeds.emails
        permission = seeds.permission
        for model in models:
            auth_token = authenticate(username=user, password=password)
            handler = SpawnHandler(auth_token)
            handler.model_id = model.model_id
            handler.progress.mark_spawned(model_id=model.model_id)
            handler.progress.ticker = model.ticker
            handler.tag(tags=tags)
            handler.share(emails=emails, permission=permission)
            progress.append(handler.progress)
        return progress
