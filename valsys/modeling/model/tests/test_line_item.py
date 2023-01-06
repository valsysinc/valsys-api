from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
import pytest


class TestLineItem:

    @property
    def valid_uid(self):
        return 'jkdhfgkdhg'

    @property
    def valid_name(self):
        return 'line item name'

    def test_init(self):
        uid = self.valid_uid
        name = self.valid_name
        li = LineItem(uid=uid, name=name)
        assert li.uid == uid
        assert li.name == name
        assert len(li.facts) == 0
        assert li.tags == []

    def test_from_json_no_facts_no_tags(self):
        uid = self.valid_uid
        name = self.valid_name
        ij = {LineItem.fields.ID: uid, LineItem.fields.NAME: name}
        li_fj = LineItem.from_json(ij)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == 0
        assert li_fj.tags == []

    def test_from_json_no_facts_with_tags(self):
        uid = self.valid_uid
        name = self.valid_name
        tags = ['t1', 't2']
        ij = {
            LineItem.fields.ID: uid,
            LineItem.fields.NAME: name,
            'tags': tags
        }
        li_fj = LineItem.from_json(ij)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == 0
        assert li_fj.tags == tags

    def test_from_json_with_facts_with_tags(self):
        uid = self.valid_uid
        name = self.valid_name
        tags = ['t1', 't2']
        facts = [{LineItem.fields.ID: 42}]
        ij = {
            LineItem.fields.ID: uid,
            LineItem.fields.NAME: name,
            LineItem.fields.TAGS: tags,
            'edges': {
                'facts': facts
            }
        }
        li_fj = LineItem.from_json(ij)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == len(facts)
        assert li_fj.tags == tags

    def test_facts_for_formula_edit(self):
        uid = self.valid_uid
        name = self.valid_name
        tags = ['t1', 't2']
        facts = [{LineItem.fields.ID: 42}, {LineItem.fields.ID: 41}]
        ij = {
            LineItem.fields.ID: uid,
            LineItem.fields.NAME: name,
            LineItem.fields.TAGS: tags,
            'edges': {
                'facts': facts
            }
        }
        li_fj = LineItem.from_json(ij)
        ffe = li_fj.facts_for_formula_edit()
        assert len(ffe) == 2
        expected_fields = [
            Fact.fields.UID, Fact.fields.FORMULA, Fact.fields.PERIOD,
            Fact.fields.IDENTIFIER
        ]
        for f in ffe:
            assert set(f.keys()).intersection(set(expected_fields)) == set(
                f.keys())

    def test_replace_fact_ok(self):
        uid = self.valid_uid
        name = self.valid_name
        facts = [{LineItem.fields.ID: 42}, {LineItem.fields.ID: 41}]
        ij = {
            LineItem.fields.ID: uid,
            LineItem.fields.NAME: name,
            'edges': {
                'facts': facts
            }
        }
        li_fj = LineItem.from_json(ij)
        assert len(li_fj.facts) == 2
        new_fact_index = 0
        new_fact = Fact(uid=92,
                        identifier='1',
                        formula='42',
                        period=1,
                        value=1,
                        fmt='1')
        li_fj.replace_fact(new_fact_index, new_fact)
        assert len(li_fj.facts) == 2
        assert li_fj.facts[new_fact_index] == new_fact

    def test_replace_fact_invalid_index(self):
        uid = self.valid_uid
        name = self.valid_name

        facts = [{LineItem.fields.ID: 42}, {LineItem.fields.ID: 41}]
        ij = {
            LineItem.fields.ID: uid,
            LineItem.fields.NAME: name,
            'edges': {
                'facts': facts
            }
        }
        li_fj = LineItem.from_json(ij)
        assert len(li_fj.facts) == 2
        new_fact_index = 2
        new_fact = Fact(uid=92,
                        identifier='1',
                        formula='42',
                        period=1,
                        value=1,
                        fmt='1')
        with pytest.raises(Exception) as err:
            li_fj.replace_fact(new_fact_index, new_fact)
        assert str(new_fact_index) in str(err)
