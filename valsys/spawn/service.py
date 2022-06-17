import json
import requests
from valsys.auth.service import authenticate
from valsys.config import URL_USERS_MODELS, VALSYS_TEAM_SUPPORT, API_USERNAME, API_PASSWORD
from valsys.modeling.service import tag_models, share_model
from valsys.spawn.socket_handler import SocketHandler, States
from collections import namedtuple

from valsys.auth.service import auth_headers
from valsys.spawn.models import ModelConfiguration
HIST_PERIOD, PROJ_PERIOD = 5, 11


def spawn_from_spark():
    model_id_lst = []
    for tbl in list(spark.catalog.listTables("model_engine")):
        if "valsys_machine_models" == tbl.name:
            model_id_lst = [x.model_id for x in spark.read.table(
                "model_engine.valsys_machine_models").select('model_id').drop_duplicates().collect()]

    if len(model_id_lst) > 0:
        username = "overlord@cppib.com"
        password = "DDIOverlord!23"

    auth_token = authenticate(username, password)

    # authenticated header
    headers = auth_headers(auth_token)

    # make request

    body = {
        "models": model_id_lst,
    }
    response = requests.delete(
        url=URL_USERS_MODELS, headers=headers, data=json.dumps(body))
    print("models dropped")
    spark.sql("DROP TABLE if exists model_engine.valsys_machine_models")
    dbutils.fs.rm(
        "s3a://cppib-iai-workspace/datalake/model_engine/valsys_machine_models.delta", recurse=True)
    df = spark.read.table("model_engine.key_drivers").filter(
        "type = 'machine'")
    df = df.select(df.ticker, df.source, df.template_id).drop_duplicates()

    df1 = spark.read.table("model_engine.latest_period").filter(
        'periodTypeId=1').drop("companyName")
    bbg_ciq_map = spark.read.table("model_engine.bbg_ciq_map")
    # ciqcompany = spark.read.table("xpressfeed.ciqCompany").select("companyId", "simpleIndustryId").distinct()
    # ciqindustry = spark.read.table("xpressfeed.ciq_industry_mapping").select("simpleIndustryId", "IndustryGroup")

    df_final = df.join(df1, [df.ticker == df1.ticker], how="left").select(
        df.ticker, df.source, df.template_id, df1.fiscalYear).distinct()
    df_final = df_final.join(bbg_ciq_map, ["ticker"])

    model_seeds = [namedtuple('X', df_final.columns)(*row)
                   for row in df_final.collect()]
    spawn_model_info = spawn(model_seeds)
    model_df = spark.createDataFrame(pd.DataFrame(spawn_model_info))
    tbl_info = {
        'table_name': 'model_engine.valsys_machine_models',
        's3_path': 's3a://cppib-iai-workspace/datalake/model_engine/valsys_machine_models.delta',
        'format': 'delta'
    }
    model_df.coalesce(1).write.saveAsTable(
        tbl_info["table_name"], mode="append", format=tbl_info["format"], path=tbl_info["s3_path"])


def spawn(model_seeds):

    model_configurations = []
    hist_period = HIST_PERIOD
    proj_period = PROJ_PERIOD
    for row in model_seeds:
        configuration = ModelConfiguration.from_row(
            row, proj_period, hist_period)
        model_configurations.append(configuration)

    # , "sbessey@cppib.com", "kurtkang@cppib.com", "ngill@cppib.com", "nellery@cppib.com", "rbosshard@cppib.com", "jteng@cppib.com",
    emails_to_share_to = VALSYS_TEAM_SUPPORT
    # "amohammad@cppib.com", "sgoyal@cppib.com", "apatil@cppib.com", "kgehlaut@cppib.com", "msawant@cppib.com", "dchan@cppib.com", "emuceniece@cppib.com", "katieyang@cppib.com"]

    tags = ["DDI Machine Model"]
    permission = "edit"

    # Create the models and saving model id
    spawn_model_info = []

    if len(model_configurations) > 0:

        for i, config in enumerate(model_configurations):

            print("({} of {}) - Creating model for ticker: {}, source: {}".format(i+1,
                                                                                  len(model_configurations), config["ticker"], config["variables"]["INTERNAL_SOURCE"]))

            if i % 10 == 0:
                auth_token = authenticate(
                    username=API_USERNAME, password=API_PASSWORD)

            config_dict = config.copy()
            config_dict["keydriver_source"] = config["variables"]["INTERNAL_SOURCE"]
            config_dict.pop("variables")

            handler = SocketHandler(config, auth_token=auth_token)
            handler.run()

            while True:
                if handler.state == States.COMPLETE:
                    if handler.error != None:
                        print("error building model:", handler.error)
                        if handler.timeout == True and config.get("retry") != True:
                            config["retry"] = True
                            model_configurations.append(config)
                    elif handler.resp != None:
                        model_id = handler.resp["data"]["uid"]

                        config_dict["model_id"] = model_id

                        # tag models
                        tag_models(model_id, tags, auth_token)

                        # share models
                        for email in emails_to_share_to:
                            share_model(model_id, email,
                                        permission, auth_token)

                        spawn_model_info.append(config_dict)

                        time.sleep(1)

                    break
    return spawn_model_info
