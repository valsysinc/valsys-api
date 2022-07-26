from dataclasses import dataclass, field
from typing import List
from unittest import mock

import pytest

from valsys.spawn.service import ValsysSpawn, spawn_models

MODULE_PREFIX = "valsys.spawn.service"


@dataclass
class FakeModelSpawnConfigs:
    configs: List[str] = field(default_factory=list)

    def __iter__(self):
        for c in self.configs:
            yield c

    @classmethod
    def create(cls, count=1):
        return cls(configs=[str(i) for i in range(0, count)])


class TestSpawnModels:

    def test_no_configs(self):
        sp = spawn_models(FakeModelSpawnConfigs.create(count=0))
        assert len(sp.processes) == 0

    @mock.patch(f"{MODULE_PREFIX}.spawn_models_same_template_periods")
    def test_with_configs(self, mock_spawn_models_same_template_periods):
        fake_configs_count = 5
        fake_spawned_count = 2
        cfgs = FakeModelSpawnConfigs.create(count=fake_configs_count)

        mock_spawn_models_same_template_periods.return_value = [
            i for i in range(fake_spawned_count)
        ]
        sp = spawn_models(cfgs)

        assert len(sp.processes) == fake_configs_count * fake_spawned_count


class TestValsysSpawn:

    @mock.patch(f"{MODULE_PREFIX}.spawn_models")
    def test_spawn_models(self, mock_spawn_models):
        cfg = 42
        mock_return = mock.MagicMock()
        mock_spawn_models.return_value = mock_return
        assert ValsysSpawn.spawn_models(cfg) == mock_return
        mock_spawn_models.assert_called_once_with(cfg)

    @pytest.mark.parametrize("exception",
                             [ValueError, KeyError, NotImplementedError])
    @mock.patch(f"{MODULE_PREFIX}.spawn_models")
    @mock.patch(f"{MODULE_PREFIX}.logger.exception")
    def test_spawn_models_raises(self, mock_logger, mock_spawn_models,
                                 exception):
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
