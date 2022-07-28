import datetime
import getpass

import pyfiglet

from valsys.auth.authenticate import authenticate2
from valsys.config.env import ENV_ROOT, EnvFiles, get_envfiles
from valsys.config.version import VERSION
from valsys.utils.service import does_file_exist, ensure_dir


class InvalidCredentialsException(Exception):
    pass


class InvalidURLException(Exception):
    pass


def gen_login_url(base: str) -> str:
    return f"{base}/users/login"


def try_login(base: str, user: str, password: str) -> bool:
    try:
        authenticate2(user, password, url=gen_login_url(base))
    except NotImplementedError:
        raise
    except ValueError:
        raise


def backup_existing_file(fn):
    if not does_file_exist(fn):
        return
    now = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    new_fn = f"{fn}.{now}"
    with open(fn, 'r') as f:
        ff = f.readlines()
    with open(new_fn, 'w') as f:
        f.writelines(ff)


def write_env(env_vars, filename):

    rows = []
    for k, v in env_vars.items():
        rows.append(f"{k}={v}")
    backup_existing_file(filename)
    with open(filename, 'w') as f:
        for r in rows:
            f.write(f"{r}\n")


def gen_fields(protocol, host):
    if protocol == 'https':
        sv_pre = 'https://'
        sk_pre = 'wss://'
    else:
        sv_pre = 'http://'
        sk_pre = 'ws://'

    host = host.replace('http://', '')
    host = host.replace('https://', '')

    return {
        'VALSYS_API_SOCKET': f"{sk_pre}{host}",
        'VALSYS_API_SERVER': f"{sv_pre}{host}"
    }


def gen_creds(username, password):
    return {'VALSYS_API_USER': username, 'VALSYS_API_PASSWORD': password}


def create_env_file(username: str,
                    password: str,
                    host: str,
                    protocol: str,
                    envfiles: EnvFiles,
                    verify=True):

    fields = gen_fields(protocol, host)
    creds = gen_creds(username, password)
    base = fields.get('VALSYS_API_SERVER')
    if verify:
        try:
            try_login(base=base,
                      user=creds.get('VALSYS_API_USER'),
                      password=creds.get('VALSYS_API_PASSWORD'))
        except NotImplementedError:
            raise InvalidURLException(f"cannot connect to url={base}")
        except Exception:
            raise InvalidCredentialsException(
                f"cannot login on {base}: invalid credentials for user {username}"
            )

    ensure_dir(ENV_ROOT)
    write_env(fields, envfiles.config)
    write_env(creds, envfiles.creds)


def _login2(username: str,
            password: str,
            host: str,
            protocol: str,
            show_banner=True):
    """Login with the provided credentials."""
    if show_banner:
        print(pyfiglet.figlet_format("ValsysLogin"), f"{' '*10} v{VERSION}")
    create_env_file(username=username,
                    password=password,
                    host=host,
                    protocol=protocol,
                    envfiles=get_envfiles('local'))


def _login_cli():
    """Login, asking for the credentials via the CLI."""
    print(pyfiglet.figlet_format("ValsysLogin"), f"{' '*10} v{VERSION}")

    print('Enter your Valsys credentials when prompted')
    host = input(f'{" "*5}> Valsys host (e.g., dev-api.valsys.io): ')
    protocol = input(f'{" "*5}> Valsys protocol (e.g., https): ')
    username = input(f'{" "*5}> Valsys username: ')
    password = getpass.getpass(f'{" "*5}> Valsys password: ')

    _login2(username=username,
            password=password,
            host=host,
            protocol=protocol,
            show_banner=False)

    print('Login succesful')


if __name__ == "__main__":
    _login_cli()
