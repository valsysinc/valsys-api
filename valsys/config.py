import os
from dotenv import load_dotenv

load_dotenv()

BASE_SCK = "ws://localhost:5100"
BASE_URL = os.getenv("VALSYS_API_SERVER")
API_USERNAME = os.getenv("VALSYS_API_USER")
API_PASSWORD = os.getenv("VALSYS_API_PASSWORD")

if BASE_URL is None:
    raise ValueError('need to have VALSYS_API_SERVER environment variable')
if API_USERNAME is None:
    raise ValueError('need to have VALSYS_API_USER environment variable')
if API_PASSWORD is None:
    raise ValueError('need to have VALSYS_API_PASSWORD environment variable')