import pytest

from valsys.modeling.model.fact import Fact
from valsys.modeling.model.line_item import LineItem
from valsys.modeling.model.tests.factories import line_item_factory


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
        nfacts = 4
        li_fj = line_item_factory(uid=uid, name=name, nfacts=nfacts, tags=tags)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == nfacts
        assert li_fj.tags == tags

    def test_facts_for_formula_edit(self):

        li_fj = line_item_factory()
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
        facts = [{Fact.fields.UID: 42}, {Fact.fields.UID: 41}]
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

        facts = [{Fact.fields.UID: 42}, {Fact.fields.UID: 41}]
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

    def test_pull_fact_by_identifier_found(self):
        li_fj = line_item_factory()
        f = li_fj.pull_fact_by_identifier('fact-1')
        assert f.uid == '1'

    def test_pull_fact_by_identifier_not_found(self):
        li_fj = line_item_factory()
        assert li_fj.pull_fact_by_identifier('garbage') is None

    def test_pull_fact_by_id_found(self):
        li_fj = line_item_factory()
        f = li_fj.pull_fact_by_id('1')
        assert f.uid == '1'

    def test_pull_fact_by_id_not_found(self):
        li_fj = line_item_factory()
        assert li_fj.pull_fact_by_id('garbage') is None
