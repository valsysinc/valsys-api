from valsys.config.config import BASE_SCK, BASE_URL


class VSURL:
    """Class holding Valsys URLS."""

    LOGIN_USERS = f"{BASE_URL}/users/login"
    CONFIGS = f"{BASE_URL}/uploader/configuration"
    TEMPLATES = f"{BASE_URL}/users/model-templates"
    MODELING_MODEL_PROPERTIES = f"{BASE_URL}/modeling/model-properties"
    MODEL_INFO = f"{BASE_URL}/modeling/model-information"
    RECALC_MODEL = f"{BASE_URL}/modeling/recalculate"
    CASE = f"{BASE_URL}/modeling/case"
    DELETE_MODULE = f"{BASE_URL}/modeling/delete-module"
    ADD_MODULE = f"{BASE_URL}/modeling/add-module"
    ADD_ITEM = f"{BASE_URL}/modeling/add-item"
    EDIT_FORMAT = f"{BASE_URL}/modeling/edit-format"
    EDIT_FORMULA = f"{BASE_URL}/modeling/edit-formula"
    USERS_SHARE_MODEL = f"{BASE_URL}/users/share-model"
    USERS_MODELS = f"{BASE_URL}/users/models"

    SCK_MODELING_CREATE = f"{BASE_SCK}/modeling/create/"
    SCK_ORCHESTRATOR = f"{BASE_SCK}:5800/orchestrator/connect/"

    @classmethod
    def login(cls, base):
        return f"{base}/users/login"
