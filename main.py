import sys
import pyfiglet

from valsys.utils import logger
from valsys.config.version import NAME, VERSION


def main(args):
    print(pyfiglet.figlet_format(NAME), f"{' '*10} v{VERSION}")
    mode = args[0]
    if mode == '--inttests':
        from valsys.inttests.run import run_inttests
        run_inttests()
    elif mode == '--spawn':
        logger.info(f"start")
        from valsys.workflows.service import main_run_spawn_models
        res = main_run_spawn_models(args[1:])
        if res.has_errors:
            logger.info(f'done with errors')
        else:
            logger.info(f'done')


if __name__ == "__main__":
    main(sys.argv[1:])
