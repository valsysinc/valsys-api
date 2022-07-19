from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Tuple

from valsys.utils import logger


@dataclass
class FormulaEditConfig:
    period_name: str
    period_year: str
    formula: str

    def validate(self):
        needs = []
        if self.period_year is None:
            needs.append('periodYear')
        if self.formula is None:
            needs.append('formula')
        if len(needs) > 0:
            raise ValueError(f'need {" ".join(needs)}')

    def __post_init__(self):
        self.validate()

    @classmethod
    def from_json(cls, config):
        return cls(period_name=config.get('periodName'),
                   period_year=config.get('periodYear', None),
                   formula=config.get('formula', None))


@dataclass
class LineItemConfig:
    name: str
    order: str
    formula_edits: List[FormulaEditConfig] = field(default_factory=list)

    @classmethod
    def from_json(cls, config):
        return cls(name=config.get('name'),
                   order=config.get('order'),
                   formula_edits=[
                       FormulaEditConfig.from_json(fec)
                       for fec in config.get('formulaEdits', [])
                   ])


@dataclass
class PopulateModulesConfig:
    tickers: List[str]
    parent_module_name: str
    module_name: str
    key_metrics_config: Dict[str, Any] = field(default_factory=dict)
    model_ids: List[str] = field(default_factory=list)
    line_item_data: List[LineItemConfig] = field(default_factory=list)

    class fields:
        TICKERS = 'tickers'
        PARENT_MODULE_NAME = 'parentModuleName'
        MODULE_NAME = 'moduleName'
        KEY_METRICS_CONFIG = 'keyMetricsConfig'
        LINE_ITEMS = 'lineItems'

    def validate(self):
        if self.parent_module_name == "":
            raise ValueError(f"need {self.fields.PARENT_MODULE_NAME}")
        if self.module_name == "":
            raise ValueError(f"need {self.fields.MODULE_NAME}")

    def get_line_item_config(self, line_item_name: str) -> LineItemConfig:
        for li in self.line_item_data:
            if li.name == line_item_name:
                return li
        raise ValueError(
            f"line item with name {line_item_name} not found in config")

    def __post_init__(self):
        self.validate()

    def set_model_ids(self, model_ids: List[str]):
        self.model_ids = model_ids

    @classmethod
    def from_json(cls,
                  config: Dict[str, Any],
                  model_ids: Optional[List[str]] = None):
        return cls(
            tickers=config.get(cls.fields.TICKERS),
            parent_module_name=config.get(cls.fields.PARENT_MODULE_NAME, ''),
            module_name=config.get(cls.fields.MODULE_NAME, ''),
            key_metrics_config=config.get(cls.fields.KEY_METRICS_CONFIG),
            line_item_data=[
                LineItemConfig.from_json(li)
                for li in config.get(cls.fields.LINE_ITEMS, [])
            ],
            model_ids=model_ids or [])


@dataclass
class MasterPopulateModulesConfig:
    modules_config: List[PopulateModulesConfig] = field(default_factory=list)

    @classmethod
    def from_json(cls, config: List[Dict[str, Any]]):
        if config is None:
            return cls()
        return cls(modules_config=[
            PopulateModulesConfig.from_json(j) for j in config
        ])

    def __iter__(self):
        for cfg in self.modules_config:
            yield cfg


@dataclass
class ModelSpawnConfig:
    tickers: List[str]
    template_name: str
    hist_period: int
    proj_period: int
    tags: List[str] = field(default_factory=list)
    emails: List[str] = field(default_factory=list)

    class fields:
        TICKERS = 'tickers'
        TEMPLATE_NAME = 'templateName'
        HIST_PERIOD = 'histPeriod'
        PROJ_PERIOD = 'projPeriod'
        TAGS = 'tags'
        EMAILS = 'emails'

    def validate(self):
        if len(self.tickers) == 0:
            raise ValueError(f'need {self.fields.TICKERS}')
        if self.template_name == "":
            raise ValueError(f'need a {self.fields.TEMPLATE_NAME}')
        if self.hist_period is None:
            raise ValueError(f'need {self.fields.HIST_PERIOD}')
        if self.proj_period is None:
            raise ValueError(f'need {self.fields.PROJ_PERIOD}')

    def __post_init__(self):
        self.validate()

    @classmethod
    def from_json(cls, spawn_config):
        return cls(
            tickers=spawn_config.get(cls.fields.TICKERS, []),
            template_name=spawn_config.get(cls.fields.TEMPLATE_NAME),
            hist_period=spawn_config.get(cls.fields.HIST_PERIOD, None),
            proj_period=spawn_config.get(cls.fields.PROJ_PERIOD, None),
            tags=spawn_config.get(cls.fields.TAGS, []),
            emails=spawn_config.get(cls.fields.EMAILS, []),
        )

    def jsonify(self):
        return {
            self.fields.TICKERS: self.tickers,
            self.fields.TEMPLATE_NAME: self.template_name,
            self.fields.HIST_PERIOD: self.hist_period,
            self.fields.PROJ_PERIOD: self.proj_period,
            self.fields.TAGS: self.tags,
            self.fields.EMAILS: self.emails
        }


@dataclass
class ModelSpawnConfigs:
    configs: List[ModelSpawnConfig] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: List[Dict[str, Any]]):
        return cls(configs=[ModelSpawnConfig.from_json(cfg) for cfg in data])

    def __iter__(self):
        for cfg in self.configs:
            yield cfg


@dataclass
class SpawnProgress:
    model_id: str = ""
    ticker: str = ""
    spawned: bool = False
    tagged: bool = False
    shared: bool = False
    spawn_error: Exception = None
    tag_error: Exception = None
    share_error: Exception = None
    shared_to: List[Tuple[str,
                          Optional[Exception]]] = field(default_factory=list)
    modules: List[Any] = field(default_factory=list)

    @property
    def all_complete(self):
        return self.spawned and self.tagged and self.shared

    def mark_tagged(self, err=None):
        if err is None:
            self.tagged = True
        self.tag_error = err

    def mark_shared(self, email: str, permission: str, err=None):
        if err is None:
            self.shared = True
        self.shared_to.append((email, permission, err))

    def mark_spawned(self, model_id: str = None, err=None):
        if err is None:
            self.spawned = True
            self.model_id = model_id
        else:
            self.spawn_error = err

    def jsonify(self, detail=False):
        """Returns a json representation of the progress;

        If `detail=True`, then any error messages are returned as well.

        `detail=False` by default.
        """
        j = {
            "modelID": self.model_id,
            "ticker": self.ticker,
            "spawned": self.spawned,
            "tagged": self.tagged,
            "shared": self.shared,
            "modules": self.modules
        }
        if detail:
            j.update({
                "spawnError":
                str(self.spawn_error or ""),
                "tagError":
                str(self.tag_error or ""),
                "sharedTo": [{
                    "email": e,
                    "permission": p,
                    "error": str(err or "")
                } for e, p, err in self.shared_to],
            })
        return j


@dataclass
class SpawnedModels:
    options: Dict[str, Any] = field(default_factory=dict)
    processes: List[SpawnProgress] = field(default_factory=list)
    verbose: bool = False

    def __post_init__(self):
        self.verbose = self.options.get("verbose", False)

    def add_populated_modules(self, pmc_rep):
        for m in pmc_rep.meta:
            self.add_modules_to_model(model_id=m.get('uid'),
                                      modules=m.get('modules'))

    def add_modules_to_model(self, model_id, modules):
        for p in self.processes:
            if p.model_id == model_id:
                p.modules = modules
                return

    def append(self, process: SpawnProgress):
        self.processes.append(process)
        if self.verbose:
            logger.info(process.jsonify(detail=True))

    def __iter__(self) -> Iterator[SpawnProgress]:
        for p in self.processes:
            yield p

    @property
    def spawned_models(self):
        return [p for p in self if p.spawned]

    @property
    def spawned_tickers(self):
        return [p.ticker for p in self.spawned_models]

    @property
    def has_errors(self):
        return len(self.spawned_models) == 0

    def spawned_model_ids_for_tickers(self, tickers: List[str]) -> List[str]:
        """Return a list of modelIDs that:

        a) have been spawned successfully, and,
        b) are in the list of provided tickers.
        """
        return [m.model_id for m in self.spawned_models if m.ticker in tickers]


@dataclass
class PopulatedModules:
    meta: List[Any] = field(default_factory=list)

    def add_model(self, model_id, case_name):
        self.meta.append({'uid': model_id, 'case': case_name, 'modules': []})

    def get_model_meta(self, model_id):
        for model_meta in self.meta:
            if model_meta.get('uid') == model_id:
                return model_meta

    def get_module_meta(self, model_meta, module_id):
        for module_meta in model_meta['modules']:
            if module_meta.get('uid') == module_id:
                return module_meta

    def add_module_to_model(self, model_id, module_id, name, uid_parent):
        model_meta = self.get_model_meta(model_id=model_id)
        model_meta['modules'].append({
            'uid': module_id,
            'name': name,
            'uid_parent': uid_parent,
            'line_items': []
        })

    def add_line_item_to_module(self, model_id, module_id, line_item_uid,
                                line_item_name):
        model_meta = self.get_model_meta(model_id=model_id)
        module_meta = self.get_module_meta(model_meta, module_id)
        module_meta['line_items'].append({
            'name': line_item_name,
            'uid': line_item_uid,
            'processes': []
        })

    def add_process_to_line_item(self, model_id, module_id, line_item_uid,
                                 proc_name):
        model_meta = self.get_model_meta(model_id=model_id)
        module_meta = self.get_module_meta(model_meta, module_id)
        for li in module_meta['line_items']:
            if li['uid'] == line_item_uid:
                li['processes'].append(proc_name)
                return
