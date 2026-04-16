#!/usr/bin/env bash

py -m venv .venv
source .venv/Scripts/activate

pip install -r requirements.txt

py manage.py runserver
