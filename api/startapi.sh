#!/usr/bin/env bash
cd /opt/api.stored.cc
gunicorn --workers 1 -b 0.0.0.0:8080 main:api --reload


