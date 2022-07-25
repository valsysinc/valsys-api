import datetime
import getpass

import pyfiglet

from valsys.auth.authenticate import authenticate2
from valsys.config.env import ENV_ROOT, EnvFiles, get_envfiles
from valsys.config.version import VERSION
from valsys.utils.service import does_file_exist, ensure_dir


class InvalidCredentialsException(Exception):
    pass


def gen_login_url(base: str) -> str:
    return f"{base}/users/login"


def try_login(base: str, user: str, password: str) -> bool:
    try:
        authenticate2(user, password, url=gen_login_url(base))
        return True
    except Exception:
        return False


def backup_existing_file(fn):
    if not does_file_exist(fn):
        return
    now = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    new_fn = f"{fn}.{now}"
    print(f"backing up existing credentials file to {new_fn}")
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


def create_env_file(username: str,
                    password: str,
                    envfiles: EnvFiles,
                    verify=True):
    fields = {
        'VALSYS_API_SOCKET': 'wss://dev-api.valsys.io',
        'VALSYS_API_SERVER': 'https://dev-api.valsys.io'
    }
    creds = {'VALSYS_API_USER': username, 'VALSYS_API_PASSWORD': password}
    if verify and not try_login(base=fields.get('VALSYS_API_SERVER'),
                                user=creds.get('VALSYS_API_USER'),
                                password=creds.get('VALSYS_API_PASSWORD')):
        raise InvalidCredentialsException(
            f"cannot login on {fields.get('VALSYS_API_SERVER')}: invalid credentials for user {username}"
        )

    ensure_dir(ENV_ROOT)
    write_env(fields, envfiles.config)
    write_env(creds, envfiles.creds)


def _login2(username: str, password: str, show_banner=True):
    """Login with the provided credentials."""
    if show_banner:
        print(pyfiglet.figlet_format("ValsysLogin"), f"{' '*10} v{VERSION}")
    create_env_file(username=username,
                    password=password,
                    envfiles=get_envfiles('local'))
    print('login succesful')
    print()


def _login_cli():
    """Login, asking for the credentials via the CLI."""
    print(pyfiglet.figlet_format("ValsysLogin"), f"{' '*10} v{VERSION}")

    print('Please enter your Valsys credentials when prompted:')
    username = input('    > Valsys username: ')
    password = getpass.getpass('    > Valsys password: ')
    _login2(username=username, password=password, show_banner=False)


if __name__ == "__main__":
    _login_cli()
