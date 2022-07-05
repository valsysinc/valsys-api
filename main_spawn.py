"""Driver example for spawning models"""
from valsys.spawn.service import spawn

spawner_report = spawn({
    'tickers': ["BLIN", "BWXT"],
    'templateName': "dcf-standard",
    'histPeriod': 2,
    'projPeriod': 3,
    'tags': ["t1"],
    'emails': ["j@me.com"]
})

spawned_model_ids = spawner_report.spawned_model_ids