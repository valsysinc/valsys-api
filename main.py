import sys
import pyfiglet

from valsys.utils import logger
from valsys.version import NAME, VERSION

from valsys.workflows.service import main_run_spawn_models


def main(args):
    print(pyfiglet.figlet_format(NAME), f"{' '*10} v{VERSION}")
    mode = args[0]
    if mode == '--spawn':
        logger.info(f"start")
        res = main_run_spawn_models(args[1:])
        if res.has_errors:
            logger.info(f'done with errors')
        else:
            logger.info(f'done')


if __name__ == "__main__":
    main(sys.argv[1:])
