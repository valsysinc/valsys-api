from typing import List, Tuple
import json
import time
from valsys.modeling.service import edit_format, edit_formula, pull_case, pull_model_information, add_item, add_child_module
from valsys.modeling.model.line_item import LineItem

parent_module_name = "Key Drivers (Input)"
module_name = "Operating Model"

key_metrics = [
    "Revenue Growth, %", "Gross Margin, %", "SG&A / sales", "R&D / sales",
    "Capex / sales"
]
key_metrics_format = {
    "fontWeight": "bold",
    "fontStyle": "normal",
    "textAlign": "right",
    "textDecoration": "none",
    "valFormat": "Percentage",
    "unit": "Raw",
    "decimalPlaces": 1
}

# List of model IDs
model_ids: List[str] = []

for model_id in model_ids:

    # Pull the first case uid
    case_id = pull_model_information(model_id)
    # Pull the case data, the case returned holds the model data packaged as a Case object

    case = pull_case(case_id)
    # Select the income statement module as we want to add a new module as a revenue driver
    root_module = case.pull_module(parent_module_name)

    # Create module
    new_module = add_child_module(parent_module_id=root_module.uid,
                                  name=module_name,
                                  model_id=model_id,
                                  case_id=case_id)

    # List of item name and item order in a Tuple.
    item_data: List[Tuple[str, int]] = []

    module_line_items: List[LineItem] = []

    for item_name, item_order in item_data:
        item_obj: LineItem = add_item(case_id=case_id,
                                      model_id=model_id,
                                      item_name=item_name,
                                      item_order=item_order,
                                      module_id=new_module.uid)
        if item_name in key_metrics:

            for idx, cell in enumerate(item_obj.facts):
                cell.fmt = json.dumps(key_metrics_format)
                item_obj.facts[idx] = cell
            edit_format(case_id=case_id,
                        model_id=model_id,
                        facts=item_obj.facts_for_format_edit())

        module_line_items.append(item_obj)

    id_lst = []
    for line_item in module_line_items:
        item_obj = line_item
        kpi_name = line_item.name

        # period_name, period_year, formula
        tmp_pdf: List[Tuple[str, str, str]] = []

        if len(tmp_pdf) == 0:
            continue
        for idx, cell in enumerate(item_obj.facts):
            for period_name, period_year, formula in tmp_pdf:
                if cell.period == int(period_year):
                    cell.formula = formula
            item_obj.facts[idx] = cell

        edit_formula(case_id, model_id, item_obj.facts_for_formula_edit())

    time.sleep(1)
