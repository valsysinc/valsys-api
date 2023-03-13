from valsys.modeling.utils import check_success, module_from_resp
from valsys.modeling.vars import Resp, Vars
import pytest
from unittest import mock
from valsys.modeling.model.module import Module

MODULE_PREFIX = "valsys.modeling.utils"


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


class TestModuleFromResp:

    @mock.patch(f"{MODULE_PREFIX}.Module.from_json")
    def test_works_ok(self, mock_from_json):
        resp = {Resp.DATA: {Resp.MODULE: {Module.fields.NAME: 'Name'}}}
        m = module_from_resp(resp)
        assert mock_from_json.called_once_with(
            resp.get(Resp.DATA).get(Resp.MODULE))
        assert m == mock_from_json.return_value
