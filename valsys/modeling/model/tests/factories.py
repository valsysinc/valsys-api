from valsys.modeling.model.case import Case
from valsys.modeling.model.module import Module
from valsys.modeling.model.model import Model
from valsys.modeling.model.line_item import LineItem


def model_factory(model_id='uid42',
                  nmodules=2,
                  nchild_modules=1,
                  nline_items=1):

    cid = '1'
    start_period = 2019

    modules = []
    for m in range(nmodules):
        parent_module_name = f"module {m}"
        parent_module_id = str(m)
        child_module_names = []
        for cmn in range(nchild_modules):
            child_module_names.append((f"{parent_module_id}{cmn}",
                                       f"{parent_module_name} child {cmn}"))
        liinfo = []
        for li in range(nline_items):
            liinfo.append(
                (f"{parent_module_id}l{li}", f"{parent_module_name} li {li}"))
        modules.append({
            Module.fields.ID: parent_module_id,
            Module.fields.NAME: parent_module_name,
            Module.fields.MODULE_START: start_period,
            Module.fields.EDGES: {
                Module.fields.LINE_ITEMS: [{
                    LineItem.fields.ID: liid,
                    LineItem.fields.NAME: linm
                } for liid, linm in liinfo],
                Module.fields.CHILD_MODULES: [{
                    Module.fields.ID:
                    cid,
                    Module.fields.NAME:
                    cmn,
                    Module.fields.MODULE_START:
                    start_period
                } for cid, cmn in child_module_names]
            }
        })

    return Model.from_json({
        Model.fields.ID: model_id,
        Model.fields.EDGES: {
            Model.fields.CASES: [{
                Case.fields.ID: cid,
                Case.fields.START_PERIOD: start_period,
                Case.fields.EDGES: {
                    Case.fields.MODULES: modules
                }
            }]
        }
    })
