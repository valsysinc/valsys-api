import logging
from valsys.utils.service import ensure_dir

LOGS_DIR = "logs"

ensure_dir(LOGS_DIR)

LOG_FILE = f"{LOGS_DIR}/general.log"
LOG_FILE_ERR = f"{LOGS_DIR}/error.log"
LOG_ID = "SPAWN"
logger = logging.getLogger(LOG_ID)
logger.setLevel(logging.DEBUG)
FORMAT = "[%(asctime)s] %(name)s %(levelname)s - %(message)s"
FORMAT_DATE = "%d-%m-%y %H:%M:%S"

screen_handler = logging.StreamHandler()
screen_handler.setLevel(logging.INFO)
screen_handler.setFormatter(logging.Formatter(FORMAT, datefmt=FORMAT_DATE))

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(FORMAT, datefmt=FORMAT_DATE))

err_file_handler = logging.FileHandler(LOG_FILE_ERR)
err_file_handler.setLevel(logging.ERROR)
err_file_handler.setFormatter(logging.Formatter(FORMAT, datefmt=FORMAT_DATE))


logger.addHandler(screen_handler)
logger.addHandler(file_handler)
logger.addHandler(err_file_handler)
