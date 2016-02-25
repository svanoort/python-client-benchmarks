#!/bin/bash
echo 'Beginning local batch bencharks'
mkdir results || true

echo 'Running PING test to stress just the connections'
python benchmark.py --cycles 10000 --url http://127.0.0.1:5000/ping --output-file results/local-by-ip-ping.csv

echo 'Running variable length response benchmarks'
python benchmark.py --cycles 10000 --url http://127.0.0.1:5000/length/1024 --output-file results/local-by-ip-1k.csv
python benchmark.py --cycles 10000 --url http://127.0.0.1:5000/length/4096 --output-file results/local-by-ip-4k.csv
python benchmark.py --cycles 10000 --url http://127.0.0.1:5000/length/8192 --output-file results/local-by-ip-8k.csv
python benchmark.py --cycles 10000 --url http://127.0.0.1:5000/length/32768 --output-file results/local-by-ip-32k.csv
python benchmark.py --cycles 10000 --url http://127.0.0.1:5000/length/131072 --output-file results/local-by-ip-128k.csv