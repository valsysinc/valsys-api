from valsys.config.config import BASE_ORCH, BASE_SCK, BASE_URL


class VSURL:
    """Class holding Valsys URLS."""

    CONFIGS = f"{BASE_URL}/uploader/configuration"

    HEALTH = f"{BASE_URL}/modeling/health"

    MODEL_INFO = f"{BASE_URL}/modeling/view/models"
    PULL_MODEL = f"{BASE_URL}/modeling/view/model"
    CASE = f"{BASE_URL}/modeling/case"

    COPY_MODEL = f"{BASE_URL}/modeling/edit/copy-model"
    RECALC_MODEL = f"{BASE_URL}/modeling/edit/recalculate"
    MODELING_MODEL_PROPERTIES = f"{BASE_URL}/modeling/edit/model-properties"

    ADD_COLUMN = f"{BASE_URL}/modeling/edit/add-column"
    DELETE_COLUMN = f"{BASE_URL}/modeling/edit/delete-column"

    RENAME_MODULE = f"{BASE_URL}/modeling/edit/module"
    REORDER_MODULE = f"{BASE_URL}/modeling/edit/reorder-module"
    DELETE_MODULE = f"{BASE_URL}/modeling/edit/delete-module"
    ADD_MODULE = f"{BASE_URL}/modeling/edit/add-module"

    ADD_ITEM = f"{BASE_URL}/modeling/edit/add-item"
    DELETE_ITEM = f"{BASE_URL}/modeling/edit/delete-item"
    EDIT_LINE_ITEMS = f"{BASE_URL}/modeling/edit/items"
    ADD_ITEM_TAGS = f"{BASE_URL}/modeling/edit/update-tags"

    EDIT_FORMAT = f"{BASE_URL}/modeling/edit/format"
    EDIT_FORMULA = f"{BASE_URL}/modeling/edit/formula"

    SIM_SIMULATION = f"{BASE_URL}/modeling/simulations/simulation"
    SIM_GROUP_DATA = f"{BASE_URL}/modeling/simulations/group-data"
    SIM_OUTPUT_VARIABLES = f"{BASE_URL}/modeling/simulations/output-variables"

    SCK_MODELING_CREATE = f"{BASE_SCK}/modeling/create/"
    SCK_ORCHESTRATOR = f"{BASE_ORCH}/orchestrator/connect/"

    USERS_SHARE_MODEL = f"{BASE_URL}/users/share-model"
    USERS_MODELS = f"{BASE_URL}/users/models"
    USERS_GROUPS = f"{BASE_URL}/users/groups"
    USERS_GROUP = f"{BASE_URL}/users/group"
    USERS_UPDATE_GROUP = f"{BASE_URL}/users/update-group"
    USERS_FILTER_HISTORY = f"{BASE_URL}/users/filter-history"
    LOGIN_USERS = f"{BASE_URL}/users/login"
    TEMPLATES = f"{BASE_URL}/users/model-templates"

    @classmethod
    def login(cls, base):
        return f"{base}/users/login"
