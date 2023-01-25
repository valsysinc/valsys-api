import os
import sys
import pyfiglet

from valsys.config.version import NAME, VERSION

VALID_MODES = {
    'LOGIN': '--login',
    "INTTESTS": '--inttests',
    "SPAWN": "--spawn"
}


def main(args):

    mode = args[0]
    if mode == VALID_MODES['LOGIN']:
        from valsys.admin import login
        login()
    elif mode == VALID_MODES['INTTESTS']:
        print("ARGS >>", args)
        if len(args) == 7:
            os.environ['VALSYS_API_BUILD'] = 'inttest'
            os.environ['VALSYS_API_SOCKET_ORCH'] = args[1]
            os.environ['VALSYS_API_SOCKET'] = args[2]
            os.environ['VALSYS_API_SERVER'] = args[3]
            os.environ['VALSYS_API_USER'] = args[4]
            os.environ['VALSYS_API_PASSWORD'] = args[5]
            opts = args[6:]
        else:
            os.environ['VALSYS_API_BUILD'] = 'inttest'
            os.environ['VALSYS_API_SOCKET'] = args[1]
            os.environ['VALSYS_API_SERVER'] = args[2]
            os.environ['VALSYS_API_USER'] = args[3]
            os.environ['VALSYS_API_PASSWORD'] = args[4]
            opts = args[5:]

        from valsys.inttests.run import run_workflows
        print(pyfiglet.figlet_format(NAME), f"{' '*10} v{VERSION}")
        run_workflows(opts)
    elif mode == VALID_MODES['SPAWN']:
        from valsys.utils import logger
        logger.info(f"start")
        from valsys.workflows.service import run_spawn_models_from_file
        print(pyfiglet.figlet_format(NAME), f"{' '*10} v{VERSION}")
        res = run_spawn_models_from_file(config_filename=args[1])
        if res.has_errors:
            logger.info(f'done with errors')
        else:
            logger.info(f'done')
    else:
        raise NotImplementedError(f"invalid mode: {mode}")


if __name__ == "__main__":
    main(sys.argv[1:])
