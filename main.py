import sys
import json
import pyfiglet
from valsys.spawn.service import spawn
from valsys.version import VERSION, NAME


def main(args):
    mode = 'spawn_models'
    print(pyfiglet.figlet_format(NAME), f"{' '*10} mode={mode} v{VERSION}")
    if mode == 'spawn_models':
        config_filename = args[0]
        with open(config_filename, "r") as file:
            spawn_config = json.loads(file.read())
        template_name = spawn_config.get('templateName', '')
        hist_period = spawn_config.get('histPeriod', None)
        proj_period = spawn_config.get('projPeriod', None)
        tickers = spawn_config.get('tickers', [])
        tags = spawn_config.get('tags', [])
        emails = spawn_config.get('emails', [])
        if len(tickers) == 0:
            raise ValueError('need tickers')
        if template_name == "":
            raise ValueError('need a templateName')
        if hist_period is None:
            raise ValueError('need histPeriod')
        if proj_period is None:
            raise ValueError('need projPeriod')
        spawner_report = spawn({
            'tickers': tickers,
            'template_name': template_name,
            'hist_period': hist_period,
            'proj_period': proj_period,
            'tags': tags,
            'emails': emails
        })
    pass


if __name__ == "__main__":
    main(sys.argv[1:])