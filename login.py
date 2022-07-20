import sys

import getpass

from valsys.env import get_envfiles, ENV_ROOT, EnvFiles
from valsys.utils.service import does_file_exist, ensure_dir
from valsys.auth.authenticate import authenticate2
import datetime
import pyfiglet
from valsys.version import NAME, VERSION


class InvalidCredentialsException(Exception):
    pass


def try_login(base, user, password):
    url = f"{base}/users/login"
    try:
        authenticate2(user, password, url=url)
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


def main():
    print(pyfiglet.figlet_format(f"{NAME}Login"), f"{' '*10} v{VERSION}")

    create_env_file(username='any',
                    password='any',
                    envfiles=get_envfiles('test'),
                    verify=False)

    print('please enter your Valsys credentials when prompted:')
    username = input('    > Valsys username: ')
    password = getpass.getpass('    > Valsys password: ')
    create_env_file(username=username,
                    password=password,
                    envfiles=get_envfiles('local'))
    print('login succesful')
    print()


if __name__ == "__main__":
    main()
