from valsys.spawn import SpawnHandler
from valsys.modeling.service import pull_model_information, pull_case


model_id = "0x37b812"
model_info = pull_model_information(uid=model_id)
print(model_info.first.uid)
case = pull_case(model_info.first.uid)
print(case.uid)
