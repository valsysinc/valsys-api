import os

BASE_SCK = "ws://localhost:5100"
BASE_URL = "http://localhost:5200"

API_USERNAME = os.getenv("VALSYS_USER")  #"jonathan.pearson@valsys.io"
API_PASSWORD = os.getenv("VALSYS_PASSWORD")  #"Solaris30"

if API_USERNAME is None:
    raise ValueError('need to have VALSYS_USER environment variable')
if API_PASSWORD is None:
    raise ValueError('need to have VALSYS_PASSWORD environment variable')