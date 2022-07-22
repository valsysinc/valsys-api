#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "installation complete"
echo "login before using the library"