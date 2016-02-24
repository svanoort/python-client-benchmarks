#!/bin/bash
# Runs on localhost:5000/ping
gunicorn app:app -b 0.0.0.0:5000 -w 8 -k gevent