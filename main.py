from typing import List
from pyspark.sql import SparkSession
from valsys.config import VALSYS_TEAM_SUPPORT, SPARK, S3_MODEL_INFO
from valsys.seeds.service import generate_model_configurations
from valsys.seeds.storage import get_model_seeds_from_spark
from valsys.spawn.service import spawn_models
from valsys.spawn.storage import save_model_info_to_spark

APP_NAME = None
spark = SparkSession.builder.appName(APP_NAME).getOrCreate()

hist_period, proj_period = 5, 11
model_tags: List[str] = ["DDI Machine Model"]
model_permission: str = "edit"
emails_to_share_to: List[str] = VALSYS_TEAM_SUPPORT


model_seeds = get_model_seeds_from_spark(spark)
model_configs = generate_model_configurations(
    model_seeds=model_seeds,
    hist_period=hist_period,
    proj_period=proj_period,
)

spawned_model_info = spawn_models(
    model_configs,
    model_tags=model_tags,
    model_permission=model_permission,
    emails_to_share_to=emails_to_share_to,
)

if spawned_model_info.has_errors:
    print("spawner errors")
    print(spawned_model_info.errors.jsonify())

save_model_info_to_spark(
    spark,
    spawned_model_info.configs,
    tbl_info={
        "table_name": f"{SPARK.CATALOG_MODEL_ENGINE}.{SPARK.TB_VALSYS_MACHINE_MODELS}",
        "s3_path": S3_MODEL_INFO,
        "format": "delta",
    },
)
