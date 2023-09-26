from valsys.modeling.model.model import Model
from valsys.inttests.runners import modeling as Runners
import time


def pluck_tags(model: Model):
    '''
    pluck_tags will pull out the first line item in the model
    that has tags and non-empty values.
    '''
    for c in model.cases:
        for m in c.modules:
            for l in m.line_items:
                if l.tags != []:
                    for f in l.facts:
                        if f.value != '':
                            return c.uid, l
    raise Exception('cannot find line item with tags')


def wait_check_formula_edited(model_id: str, line_item_id: str, fact_id: str, new_formula: str):
    attempt_number = 0
    max_tries = 10
    while True:
        attempt_number += 1
        mp1 = Runners.run_pull_model(model_id)
        li = mp1.pull_line_item(line_item_id)
        f = li.pull_fact_by_id(fact_id)
        if f.formula == new_formula:
            break
        if attempt_number > max_tries:
            raise Exception(
                f'formula tracked not changed after {attempt_number} attempts')
        time.sleep(1)
    return


def wait_check_facts_tracked(model_id: str, line_item_id: str):
    attempt_number = 0
    max_tries = 10
    while True:
        attempt_number += 1
        mp1 = Runners.run_pull_model(model_id)
        li = mp1.pull_line_item(line_item_id)
        if li.facts_tracked:
            break
        if attempt_number > max_tries:
            raise Exception(
                f'facts tracked not changed after {attempt_number} attempts')
        time.sleep(1.5)
    return
