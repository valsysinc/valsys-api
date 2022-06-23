from typing import Any, Dict, List
from valsys.auth.service import authenticate
from valsys.config import API_PASSWORD, API_USERNAME
from valsys.modeling.service import share_model, tag_models
from valsys.spawn.models import (
    ModelSeedConfigurationData,
    SpawnerErrors,
    SpawnerError,
    SpawnerReport,
)
from valsys.spawn.socket_handler import SocketHandler, States


def spawn_models(
    model_configurations: List[ModelSeedConfigurationData],
    model_tags: List[str],
    model_permission: str,
    emails_to_share_to: List[str],
) -> SpawnerReport:
    """Spawn the models;

    For each model:
    - spawn
    - tag the model
    - share the model.
    """

    # Create the models and saving model id
    spawn_model_info: List[Dict[str, Any]] = []

    if len(model_configurations) == 0:
        return []

    errors = SpawnerErrors()

    for i, config in enumerate(model_configurations):

        print(
            f"({i+1} of {len(model_configurations)}) - Creating model for ticker: {config.ticker}, source: {config.data_source}"
        )

        if i % 10 == 0:
            auth_token = authenticate(username=API_USERNAME, password=API_PASSWORD)

        config_dict = config.jsonify().copy()
        config_dict["keydriver_source"] = config.data_source
        config_dict.pop("variables")
        try:
            handler = SocketHandler(config.jsonify(), auth_token=auth_token)
            handler.run()
        except Exception as err:
            errors.append(
                SpawnerError(
                    name="spawn",
                    info={
                        "id": i,
                        "ticker": config.ticker,
                        "source": config.data_source,
                    },
                    exception=err,
                )
            )

        while True:
            if handler.state != States.COMPLETE:
                continue
            if handler.error is not None:
                print("error building model:", handler.error)
            elif handler.resp is not None:
                model_id = handler.resp["data"]["uid"]
                config_dict["model_id"] = model_id

                # tag models
                try:
                    tag_models(model_id, model_tags, auth_token)
                except Exception as err:
                    errors.append(
                        SpawnerError(
                            name="tag_models",
                            info={"id": i, "modelID": model_id},
                            exception=err,
                        )
                    )

                # share models
                for email in emails_to_share_to:
                    try:
                        share_model(model_id, email, model_permission, auth_token)
                    except Exception as err:
                        errors.append(
                            SpawnerError(
                                name="share_model",
                                info={"id": i, "modelID": model_id, "email": email},
                                exception=err,
                            )
                        )
                spawn_model_info.append(config_dict)

            break
    return SpawnerReport(configs=spawn_model_info, errors=errors)
