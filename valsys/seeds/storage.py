
from collections import namedtuple
from typing import List
from valsys.config import (SPARK)

from valsys.spawn.models import SeedDataFrameRow

from pyspark.sql import SparkSession


def get_model_seeds_from_spark(spark: SparkSession) -> List[SeedDataFrameRow]:

    df = spark.read.table(f"{SPARK.CATALOG_MODEL_ENGINE}.{SPARK.TB_KEY_DRIVERS}").filter(
        "type = 'machine'")
    df = df.select(df.ticker, df.source, df.template_id).drop_duplicates()

    df1 = spark.read.table(f"{SPARK.CATALOG_MODEL_ENGINE}.{SPARK.TB_LATEST_PERIOD}").filter(
        'periodTypeId=1').drop("companyName")
    bbg_ciq_map = spark.read.table(
        f"{SPARK.CATALOG_MODEL_ENGINE}.{SPARK.TB_BBG_MAP}")

    df_final = df.join(df1, [df.ticker == df1.ticker],
                       how="left").select(df.ticker, df.source, df.template_id,
                                          df1.fiscalYear).distinct().join(bbg_ciq_map, ["ticker"])

    return [
        namedtuple('X', df_final.columns)(*row) for row in df_final.collect()
    ]
