#!/usr/bin/env bash

set -e # exit on error

pip3 install -r requirements.txt

python lal_web/manage.py collectstatic --noinput