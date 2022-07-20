#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp env/.env env/.env.bak
cp env/.env.test env/.env
python login.py