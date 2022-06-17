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
