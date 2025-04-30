#!/bin/bash
pip install -r requirements.txt
cd api
gunicorn --bind 0.0.0.0:$PORT app:app 