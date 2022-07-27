from valsys.config.env import get_envfiles
from valsys.admin.service import create_env_file


def main():

    create_env_file(username='any',
                    password='any',
                    protocol='any',
                    host='any',
                    envfiles=get_envfiles('test'),
                    verify=False)


if __name__ == "__main__":
    main()
