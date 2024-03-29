import os


def does_file_exist(fn:str):
    return os.path.exists(fn)

def does_dir_exist(dir: str) -> bool:
    return os.path.exists(dir)


def ensure_dir(dir: str):
    """Create the directory if it doesnt
    already exist."""
    if not does_dir_exist(dir):
        os.makedirs(dir)
