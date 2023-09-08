from valsys.config.config import BASE_ORCH, BASE_SCK, BASE_URL

MODELING = "modeling"

class VSURL:
    """Class holding Valsys URLS."""

    CONFIGS = f"{BASE_URL}/uploader/configuration"

    HEALTH = f"{BASE_URL}/{MODELING}/health"

    MODEL_INFO = f"{BASE_URL}/{MODELING}/view/models"
    PULL_MODEL = f"{BASE_URL}/{MODELING}/view/model"
    CASE = f"{BASE_URL}/{MODELING}/case"

    COPY_MODEL = f"{BASE_URL}/{MODELING}/edit/copy-model"

    RECALC_MODEL = f"{BASE_URL}/{MODELING}/edit/recalculate"
    MODELING_MODEL_PROPERTIES = f"{BASE_URL}/{MODELING}/edit/model-properties"

    ADD_COLUMN = f"{BASE_URL}/{MODELING}/edit/add-column"
    DELETE_COLUMN = f"{BASE_URL}/{MODELING}/edit/delete-column"

    RENAME_MODULE = f"{BASE_URL}/{MODELING}/edit/module"
    REORDER_MODULE = f"{BASE_URL}/{MODELING}/edit/reorder-module"
    DELETE_MODULE = f"{BASE_URL}/{MODELING}/edit/delete-module"
    ADD_MODULE = f"{BASE_URL}/{MODELING}/edit/add-module"

    ADD_ITEM = f"{BASE_URL}/{MODELING}/edit/add-item"
    DELETE_ITEM = f"{BASE_URL}/{MODELING}/edit/delete-item"
    EDIT_LINE_ITEMS = f"{BASE_URL}/{MODELING}/edit/items"
    ADD_ITEM_TAGS = f"{BASE_URL}/{MODELING}/edit/update-tags"

    EDIT_FORMAT = f"{BASE_URL}/{MODELING}/edit/format"
    EDIT_FORMULA = f"{BASE_URL}/{MODELING}/edit/formula"

    SIM_SIMULATION = f"{BASE_URL}/{MODELING}/simulations/simulation"
    SIM_GROUP_DATA = f"{BASE_URL}/{MODELING}/simulations/group-data"
    SIM_OUTPUT_VARIABLES = f"{BASE_URL}/{MODELING}/simulations/output-variables"

    VSL_QUERY = f"{BASE_URL}/{MODELING}/dsl/query"

    SCK_MODELING_CREATE = f"{BASE_SCK}/{MODELING}/create/"
    SCK_ORCHESTRATOR = f"{BASE_ORCH}/orchestrator/connect/"

    USERS_SHARE_MODEL = f"{BASE_URL}/users/share-model"
    USERS_MODELS = f"{BASE_URL}/users/models"

    USERS_GROUPS = f"{BASE_URL}/users/groups"
    USERS_GROUP = f"{BASE_URL}/users/group"
    USERS_UPDATE_GROUP = f"{BASE_URL}/users/update-group"
    USERS_FILTER_HISTORY = f"{BASE_URL}/users/filter-history"
    USERS_FILTER_HISTORY_FIELDS = f"{BASE_URL}/users/filter-history-with-fields"
    LOGIN_USERS = f"{BASE_URL}/users/login"
    TEMPLATES = f"{BASE_URL}/users/model-templates"

    

    @classmethod
    def login(cls, base):
        return f"{base}/users/login"
