from valsys.inttests.runners.utils import assert_contains

class TestAssertContains:
    def test_works_ok(self):
        mstr = ['a1', 'a2']
        tst = ['a1']
        assert_contains(mstr, tst)