from valsys.config import VALSYS_TEAM_SUPPORT, SPARK, S3_MODEL_INFO
from valsys.spawn.service import spawn_models, save_model_info_to_spark, get_model_seeds_from_spark, generate_model_configurations_from_seeds

hist_period, proj_period = 5, 11

model_tags = ["DDI Machine Model"]
model_permission = 'edit'
emails_to_share_to = VALSYS_TEAM_SUPPORT
model_configs = generate_model_configurations_from_seeds(model_seeds=get_model_seeds_from_spark(),
                                                         hist_period=hist_period,
                                                         proj_period=proj_period,)

spawned_model_info = spawn_models(model_configs,
                                  model_tags=model_tags,
                                  model_permission=model_permission,
                                  emails_to_share_to=emails_to_share_to)
save_model_info_to_spark(spawned_model_info, tbl_info={
    'table_name': f"{SPARK.CATALOG_MODEL_ENGINE}.{SPARK.TB_VALSYS_MACHINE_MODELS}",
    's3_path': S3_MODEL_INFO,
    'format': 'delta'
})
