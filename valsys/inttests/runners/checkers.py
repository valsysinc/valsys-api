from valsys.modeling.model.module import Module


def order(module: Module, line_item_id: str, expected_order: int):
    found = False
    for line_item in module.line_items:
        if line_item.uid == line_item_id:
            assert line_item.order == expected_order
            found = True
    assert found


def period(nm: Module, new_period: float):
    for line_item in nm.line_items:
        found = False
        for fact in line_item.facts:
            if fact.period == new_period:
                found = True
                break
        assert found
