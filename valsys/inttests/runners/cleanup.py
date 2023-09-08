from dataclasses import dataclass, field
from typing import Callable, List, Any, Tuple
from valsys.utils import loggerIT as logger


@dataclass
class TestsCleanUp:
    funcs: List[Tuple[Callable, List[Any]]] = field(default_factory=list)

    def register(self, f, *args, **kwargs):
        self.funcs.append((f, [args, kwargs]))

    def run(self):
        logger.info('running cleanup funcs')
        for func, params in self.funcs:
            func(*params[0], **params[1])
        logger.info('cleanup done')
