from valsys.inttests.runners.utils import assert_contains
import pytest
class TestAssertContains:
    @pytest.mark.parametrize("master,tests", 
                             [([],[]),(['a1'],['a1']),(['a1', 'a2'],  ['a1'])])
    def test_works_ok(self, master, tests):
        assert_contains(master, tests)

    @pytest.mark.parametrize("master,tests", 
                             [(['a1','a2'],['']),(['a1', 'a2'],  ['a3'])])
    def test_fails(self,  master, tests):
        
        with pytest.raises(AssertionError):
            assert_contains( master, tests)
        