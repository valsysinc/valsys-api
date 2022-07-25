from valsys.modeling.model.line_item import LineItem


class TestLineItem:

    def test_init(self):
        uid = 'jkdhfgkdhg'
        name = 'Name'
        li = LineItem(uid=uid, name=name)
        assert li.uid == uid
        assert li.name == name
        assert len(li.facts) == 0
        assert li.tags is None

    def test_from_json_no_facts_no_tags(self):
        uid = 'jkdhfgkdhg'
        name = 'Name'
        ij = {'uid': uid, 'name': name}
        li_fj = LineItem.from_json(ij)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == 0
        assert li_fj.tags is None

    def test_from_json_no_facts_with_tags(self):
        uid = 'jkdhfgkdhg'
        name = 'Name'
        tags = ['t1', 't2']
        ij = {'uid': uid, 'name': name, 'tags': tags}
        li_fj = LineItem.from_json(ij)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == 0
        assert li_fj.tags == tags

    def test_from_json_with_facts_with_tags(self):
        uid = 'jkdhfgkdhg'
        name = 'Name'
        tags = ['t1', 't2']
        facts = [{'uid': 42}]
        ij = {'uid': uid, 'name': name, 'tags': tags, 'facts': facts}
        li_fj = LineItem.from_json(ij)
        assert li_fj.uid == uid
        assert li_fj.name == name
        assert len(li_fj.facts) == len(facts)
        assert li_fj.tags == tags
