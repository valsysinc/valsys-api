from valsys.modeling.model.line_item import LineItem
from valsys.modeling.model.fact import Fact


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
        assert li.tags is None

    def test_from_json_no_facts_no_tags(self):
        uid = self.valid_uid
        name = self.valid_name
        ij = {'uid': uid, 'name': name}
        li_fj = LineItem.from_json(ij)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == 0
        assert li_fj.tags is None

    def test_from_json_no_facts_with_tags(self):
        uid = self.valid_uid
        name = self.valid_name
        tags = ['t1', 't2']
        ij = {'uid': uid, 'name': name, 'tags': tags}
        li_fj = LineItem.from_json(ij)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == 0
        assert li_fj.tags == tags

    def test_from_json_with_facts_with_tags(self):
        uid = self.valid_uid
        name = self.valid_name
        tags = ['t1', 't2']
        facts = [{'uid': 42}]
        ij = {'uid': uid, 'name': name, 'tags': tags, 'facts': facts}
        li_fj = LineItem.from_json(ij)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == len(facts)
        assert li_fj.tags == tags

    def test_facts_for_formula_edit(self):
        uid = self.valid_uid
        name = self.valid_name
        tags = ['t1', 't2']
        facts = [{'uid': 42}, {'uid': 41}]
        ij = {'uid': uid, 'name': name, 'tags': tags, 'facts': facts}
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
