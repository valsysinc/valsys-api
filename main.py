import sys
import pyfiglet

from valsys.config.version import NAME, VERSION


def main(args):

    mode = args[0]
    if mode == '--login':
        from valsys.admin import login
        login()
    elif mode == '--inttests':
        from valsys.inttests.run import run_inttests
        print(pyfiglet.figlet_format(NAME), f"{' '*10} v{VERSION}")
        run_inttests()
    elif mode == '--spawn':
        from valsys.utils import logger
        logger.info(f"start")
        from valsys.workflows.service import run_spawn_models_from_file
        print(pyfiglet.figlet_format(NAME), f"{' '*10} v{VERSION}")
        res = run_spawn_models_from_file(config_filename=args[1])
        if res.has_errors:
            logger.info(f'done with errors')
        else:
            logger.info(f'done')
    elif mode == '--create':
        from valsys.utils import logger
        logger.info(f"start")
        from valsys.workflows.service import generate_model_from_file
        print(pyfiglet.figlet_format(NAME), f"{' '*10} v{VERSION}")
        res = generate_model_from_file(config_filename=args[1])


if __name__ == "__main__":
    main(sys.argv[1:])
