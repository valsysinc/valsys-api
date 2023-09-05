import time
import os
import sys

# python tmp.py --inttests wss:dev-api.valsys.io:5800 wss:dev-api.valsys.io:5100 https://dev-api.valsys.io sb Absyks_1234 integration
# python tmp.py --inttests ws://localhost:5800 ws://localhost:5100 http://localhost:5200 sb Absyks_1234 integration

# user: test-user@valsys.io
# password: test|us3R_Passw0rd!


def run_temp_tests(args):

    os.environ['VALSYS_API_BUILD'] = 'inttest'
    os.environ['VALSYS_API_SOCKET_ORCH'] = args[1]
    os.environ['VALSYS_API_SOCKET'] = args[2]
    os.environ['VALSYS_API_SERVER'] = args[3]
    os.environ['VALSYS_API_USER'] = args[4]
    os.environ['VALSYS_API_PASSWORD'] = args[5]

    from valsys.config.config import API_PASSWORD, API_USERNAME
    from valsys.modeling.client.urls import VSURL, BASE_URL
    from valsys.modeling.client.service import new_client
    import uuid
    client = new_client()
    url = f"{BASE_URL}/modeling/sync/upload"
    payload = {'model': {
        'mode': 'CREATE',
        'createdBy': 'test-user',
        'id': str(uuid.uuid1()),
        'ticker': "PEP",
        'companyName': 'Pepsi',
        'dataSources': 'default',
        'iterations': 100,
        'precision': 0.01,
        'periodType': 'Annual',
        'forecastPeriod': 7,
        'historicalPeriod': 5,
        'startPeriod': 2015
    }}
    resp = client.post(url=url, data=payload)


if __name__ == '__main__':
    args = sys.argv[1:]

    run_temp_tests(args)
