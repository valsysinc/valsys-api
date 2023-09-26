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
        self.to_delete.append(model_id)

    def run(self):
        logger.info('running cleanup funcs')
        for func, params in self.funcs:
            func(*params[0], **params[1])
        Runners.run_delete_models(self.to_delete)
        logger.info('cleanup done')
