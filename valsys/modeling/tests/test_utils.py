from valsys.modeling.utils import check_success
from valsys.modeling.vars import Resp, Vars
import pytest


class FakeException(Exception):
    pass


class TestCheckSuccess:

    def test_works_ok(self):
        resp = {Resp.STATUS: Vars.SUCCESS}
        assert check_success(resp, None)

    def test_not_success(self):
        resp = {Resp.STATUS: 'garbage', Resp.ERROR: 'error'}
        desc = 'info'
        with pytest.raises(Exception) as err:
            check_success(resp, desc)
        assert desc in str(err)
        assert resp[Resp.ERROR] in str(err)

    def test_not_success_custom_exception(self):
        resp = {Resp.STATUS: 'garbage', Resp.ERROR: 'error'}
        custom_exception = FakeException
        desc = 'info'
        with pytest.raises(custom_exception) as err:
            check_success(resp, desc, exception=custom_exception)
        assert desc in str(err)
        assert resp[Resp.ERROR] in str(err)