#!/usr/bin/env bash

sudo apt-get install -y fonts-inconsolata
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
