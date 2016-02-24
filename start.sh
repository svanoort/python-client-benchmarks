#!/bin/bash
# Runs on localhost:5000/ping

# Slower, ~800 RPS with 50k request size by apache bench, concurrency 1
#gunicorn app:app -b 0.0.0.0:5000 -w 8 -k gevent

# Meinheld, ~1200 RPS with 50k request size on flask by apache bench, concurrency 1
# Maxes out at 1400 RPS with tiny requests, can pull up to 500 MB/s throughput with large ones (1 MB per)
gunicorn app:app -b 0.0.0.0:5000 --worker-class="egg:meinheld#gunicorn_worker" -w 8