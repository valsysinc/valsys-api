import pytest
from valsys.utils.utils import read_env
from unittest import mock

MODULE_PREFIX = "valsys.utils.utils"


class TestReadEnv:

    @mock.patch(f"{MODULE_PREFIX}.os.getenv")
    def test_works_ok(self, mock_getenv):
        varn = 'variableName'
        mock_getenv.return_value = 42
        assert read_env(varn) == 42
        mock_getenv.assert_called_with(varn)

    @mock.patch(f"{MODULE_PREFIX}.os.getenv")
    def test_not_found_required(self, mock_getenv):
        varn = 'variableName'
        mock_getenv.return_value = None
        with pytest.raises(ValueError) as err:
            read_env(varn)
        assert varn in str(err)

    @mock.patch(f"{MODULE_PREFIX}.os.getenv")
    def test_not_found_not_required(self, mock_getenv):
        varn = 'variableName'
        mock_getenv.return_value = None
        assert read_env(varn, required=False) == None
