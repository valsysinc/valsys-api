import json
from typing import List, Dict, Any
import requests
from valsys.auth.service import authenticate
from valsys.config import URL_USERS_MODELS, API_USERNAME, API_PASSWORD, API_DEL_USERNAME, API_DEL_PASSWORD, SPARK, S3_MODEL_INFO
from valsys.modeling.service import tag_models, share_model
from valsys.spawn.socket_handler import SocketHandler, States
from collections import namedtuple

from valsys.auth.service import auth_headers
from valsys.spawn.models import ModelSeedConfigurationData, SeedDataFrameRow


def get_model_ids_list():
    model_id_lst = []
    for tbl in list(spark.catalog.listTables(SPARK.CATALOG_MODEL_ENGINE)):
        if SPARK.TB_VALSYS_MACHINE_MODELS == tbl.name:
            model_id_lst = [
                x.model_id
                for x in spark.read.table(f"{SPARK.CATALOG_MODEL_ENGINE}.{SPARK.TB_VALSYS_MACHINE_MODELS}")
                .select('model_id').drop_duplicates().collect()
            ]
    return model_id_lst


def drop_existing_models():

    if model_id_lst := get_model_ids_list():
        auth_token = authenticate(API_DEL_USERNAME, API_DEL_PASSWORD)

        # make request
        body = {
            "models": model_id_lst,
        }
        response = requests.delete(url=URL_USERS_MODELS,
                                   headers=auth_headers(auth_token),
                                   data=json.dumps(body))
        print("models dropped")


def drop_machine_models_table():
    spark.sql(SPARK.SQL_DROP_VMM)


def delete_machine_models_delta():
    dbutils.fs.rm(S3_MODEL_INFO, recurse=True)


def get_model_seeds_from_spark() -> List[SeedDataFrameRow]:
    drop_existing_models()
    drop_machine_models_table()
    delete_machine_models_delta()

    df = spark.read.table("model_engine.key_drivers").filter(
        "type = 'machine'")
    df = df.select(df.ticker, df.source, df.template_id).drop_duplicates()

    df1 = spark.read.table("model_engine.latest_period").filter(
        'periodTypeId=1').drop("companyName")
    bbg_ciq_map = spark.read.table("model_engine.bbg_ciq_map")
    # ciqcompany = spark.read.table("xpressfeed.ciqCompany").select("companyId", "simpleIndustryId").distinct()
    # ciqindustry = spark.read.table("xpressfeed.ciq_industry_mapping").select("simpleIndustryId", "IndustryGroup")

    df_final = df.join(df1, [df.ticker == df1.ticker],
                       how="left").select(df.ticker, df.source, df.template_id,
                                          df1.fiscalYear).distinct()
    df_final = df_final.join(bbg_ciq_map, ["ticker"])

    return [
        namedtuple('X', df_final.columns)(*row) for row in df_final.collect()
    ]


def save_model_info_to_spark(spawn_model_info, tbl_info):

    model_df = spark.createDataFrame(pd.DataFrame(spawn_model_info))

    model_df.coalesce(1).write.saveAsTable(tbl_info["table_name"],
                                           mode="append",
                                           format=tbl_info["format"],
                                           path=tbl_info["s3_path"])


def generate_model_configurations_from_seeds(model_seeds: List[SeedDataFrameRow], proj_period, hist_period) -> List[ModelSeedConfigurationData]:
    model_configurations: List[ModelSeedConfigurationData] = []
    for row in model_seeds:
        configuration = ModelSeedConfigurationData.from_row(row, proj_period,
                                                            hist_period)
        model_configurations.append(configuration)
    return model_configurations


def spawn_models(model_configurations: List[ModelSeedConfigurationData], model_tags: List[str], model_permission: str,
                 emails_to_share_to: List[str]) -> List[Dict[str, Any]]:

    # Create the models and saving model id
    spawn_model_info: List[Dict[str, Any]] = []

    if len(model_configurations) == 0:
        return []

    for i, config in enumerate(model_configurations):

        print(f"({i+1} of {len(model_configurations)}) - Creating model for ticker: {config.ticker}, source: {config.data_source}")

        if i % 10 == 0:
            auth_token = authenticate(username=API_USERNAME,
                                      password=API_PASSWORD)

        config_dict = config.jsonify().copy()
        config_dict["keydriver_source"] = config.data_source
        config_dict.pop("variables")

        handler = SocketHandler(config.jsonify(), auth_token=auth_token)
        handler.run()

        while True:
            if handler.state != States.COMPLETE:
                continue
            if handler.error != None:
                print("error building model:", handler.error)
                if handler.timeout == True and config.get(
                        "retry") != True:
                    config["retry"] = True
                    model_configurations.append(config)
            elif handler.resp != None:
                model_id = handler.resp["data"]["uid"]

                config_dict["model_id"] = model_id

                # tag models
                tag_models(model_id, model_tags, auth_token)

                # share models
                for email in emails_to_share_to:
                    share_model(model_id, email, model_permission,
                                auth_token)

                spawn_model_info.append(config_dict)

                time.sleep(1)

            break
    return spawn_model_info
