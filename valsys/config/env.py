import os


ENV_ROOT = '.valsys-env'


class EnvFiles:
    _config: str = ''
    _creds: str = ''

    @property
    def config(self):
        return os.path.join(ENV_ROOT, self._config)

    @property
    def creds(self):
        return os.path.join(ENV_ROOT, self._creds)


class LocalEnvFiles(EnvFiles):
    _config = '.env'
    _creds = '.creds'


class TestEnvFiles(EnvFiles):
    _config = '.env.test'
    _creds = '.creds.test'


def get_envfiles(build) -> EnvFiles:

    if build == 'test':
        return TestEnvFiles()
    else:
        return LocalEnvFiles()
