import os


def read_env(varn, required=True):
    var = os.getenv(varn)
    if var is None and required is True:
        raise ValueError(f'need to have {varn} environment variable')
    return var