from unittest import mock

import pytest

from valsys.spawn.service import ValsysSpawn


MODULE_PREFIX = "valsys.spawn.service"


class TestValsysSpawn:
    @mock.patch(f"{MODULE_PREFIX}.spawn_models")
    def test_spawn_models(self, mock_spawn_models):
        cfg = 42
        mock_return = mock.MagicMock()
        mock_spawn_models.return_value = mock_return
        assert ValsysSpawn.spawn_models(cfg) == mock_return
        mock_spawn_models.assert_called_once_with(cfg)

    @pytest.mark.parametrize(
        "exception", [ValueError, KeyError, NotImplementedError]
    )
    @mock.patch(f"{MODULE_PREFIX}.spawn_models")
    @mock.patch(f"{MODULE_PREFIX}.logger.exception")
    def test_spawn_models_raises(self, mock_logger, mock_spawn_models, exception):
        cfg = 42

        mock_spawn_models.side_effect = exception
        assert ValsysSpawn.spawn_models(cfg) == None
        assert mock_logger.called_once_with(exception)

    @mock.patch(f"{MODULE_PREFIX}.populate_modules")
    def test_populate_modules(self, mock_populate_modules):
        cfg = 42
        mock_return = mock.MagicMock()
        mock_populate_modules.return_value = mock_return
        assert ValsysSpawn.populate_modules(cfg) == mock_return
        mock_populate_modules.assert_called_once_with(cfg)
