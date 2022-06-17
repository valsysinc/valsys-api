import os
BASE_URL = os.environ["BASE_URL"]
SOCKET_BASE = "wss://valsys.iai.cppib.io"

URL_LOGIN_USERS = f"{BASE_URL}users/login"
URL_MODELING_CREATE = f"{SOCKET_BASE}/modeling/create/"
URL_MODELING_MODEL_PROPERTIES = f"{BASE_URL}modeling/model-properties"
URL_USERS_SHARE_MODEL = f"{BASE_URL}users/share-model"
URL_USERS_MODELS = f"{BASE_URL}users/models"

VALSYS_TEAM_SUPPORT = ["jworthington@cppib.com", "jfuller@cppib.com"]

API_USERNAME = "sbessey@cppib.com"
API_PASSWORD = "Absyks_1234"

API_DEL_USERNAME = "overlord@cppib.com"
API_DEL_PASSWORD = "DDIOverlord!23"


class SPARK:
    CATALOG_MODEL_ENGINE = "model_engine"
    TB_VALSYS_MACHINE_MODELS = "valsys_machine_models"
    TB_KEY_DRIVERS = 'key_drivers'
    TB_LATEST_PERIOD = 'latest_period'
    TB_BBG_MAP = 'bbg_ciq_map'
    SQL_DROP_VMM = "DROP TABLE if exists model_engine.valsys_machine_models"


S3_MODEL_INFO = 's3a://cppib-iai-workspace/datalake/model_engine/valsys_machine_models.delta'
