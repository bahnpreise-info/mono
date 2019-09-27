#!/usr/bin/env bash
cd /opt/api.stored.cc
gunicorn --workers 4 -b 0.0.0.0:8080 main:api -b [::1]:8080 --reload

