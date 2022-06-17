import os
BASE_URL = os.environ["BASE_URL"]
SOCKET_BASE="wss://valsys.iai.cppib.io"

URL_LOGIN_USERS = f"{BASE_URL}users/login"
URL_MODELING_CREATE = f"{SOCKET_BASE}/modeling/create/"
URL_MODELING_MODEL_PROPERTIES = f"{BASE_URL}modeling/model-properties"
URL_USERS_SHARE_MODEL = f"{BASE_URL}users/share-model"