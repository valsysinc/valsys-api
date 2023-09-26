from dataclasses import dataclass, field
from typing import Callable, List, Any, Tuple
from valsys.utils import loggerIT as logger
from valsys.inttests.runners import modeling as Runners


@dataclass
class TestsCleanUp:
    funcs: List[Tuple[Callable, List[Any]]] = field(default_factory=list)
    to_delete: List[str] = field(default_factory=list)

    def register(self, f, *args, **kwargs):
        self.funcs.append((f, [args, kwargs]))

    def mark_model_for_deletion(self, model_id: str):
        """Provide the modelID to be deleted
        when the final clean up is `run`
        """
        self.to_delete.append(model_id)

    def run(self):
        """Run the clean up;
        Note that any models marked for deletion
        are deleted at this point."""
        logger.info('running cleanup funcs')
        for func, params in self.funcs:
            func(*params[0], **params[1])
        Runners.run_delete_models(self.to_delete)
        logger.info('cleanup done')
