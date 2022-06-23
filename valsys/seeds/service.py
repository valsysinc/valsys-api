from typing import List
from valsys.spawn.models import ModelSeedConfigurationData, SeedDataFrameRow


def generate_model_configurations(
        model_seeds: List[SeedDataFrameRow],
        proj_period, hist_period) -> List[ModelSeedConfigurationData]:
    model_configurations: List[ModelSeedConfigurationData] = []
    for row in model_seeds:
        model_configurations.append(ModelSeedConfigurationData.from_row(row, proj_period,
                                                                        hist_period))
    return model_configurations
