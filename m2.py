from valsys.modeling.service import pull_model_information, pull_case
from valsys.modeling.service import edit_format, edit_formula, pull_case, pull_model_information, add_item, add_child_module
import json
moduleConfig = [
    {
        "parentModuleName": "Income Statement",
        "moduleName": "Operating Model8",
        "keyMetricsConfig": {
            "metrics": [
                "Revenue Growth, %",
                "Gross Margin, %",
                "SG&A / sales",
                "R&D / sales",
                "Capex / sales"
            ],
            "format": {
                "fontWeight": "bold",
                "fontStyle": "normal",
                "textAlign": "right",
                "textDecoration": "none",
                "valFormat": "Percentage",
                "unit": "Raw",
                "decimalPlaces": 1
            }
        },
        "lineItems": [
            {
                "name": "Revenue Growth, %",
                "order": 2
            },
            {
                "name": "line item 2",
                "order": 1
            }
        ]
    }]

model_id = "0x3a856c"

parent_module_name = moduleConfig[0].get('parentModuleName')
module_name = moduleConfig[0].get('moduleName')
item_data = [(i.get('name'), i.get('order')) for i in moduleConfig[0].get('lineItems')]
key_metrics = moduleConfig[0].get('keyMetricsConfig').get('metrics')
key_metrics_format = moduleConfig[0].get('keyMetricsConfig').get('format')
model_info = pull_model_information(uid=model_id)
print(model_info.first.uid)
case = pull_case(model_info.first.uid)
root_module = case.pull_module(parent_module_name)
case_id = case.uid
new_module = add_child_module(parent_module_id=root_module.uid,
                              name=module_name,
                              model_id=model_id,
                              case_id=case.uid)

for item_name, item_order in item_data:
    item_obj = add_item(case_id=case_id,
                        model_id=model_id,
                        name=item_name,
                        order=item_order,
                        module_id=new_module.uid)
    if item_name in key_metrics:

        for idx, cell in enumerate(item_obj.facts):
            cell.fmt = json.dumps(key_metrics_format)
            item_obj.facts[idx] = cell
        edit_format(case_id=case_id,
                    model_id=model_id,
                    facts=item_obj.facts_for_format_edit())
