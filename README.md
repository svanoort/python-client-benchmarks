# python-client-benchmarks
Simple demonstration of benchmarking different python HTTP client tools with a trivial Flask app (returns 'pong' from http://localhost:5000/ping).

# Requirements
(pip) Install - handled by install.sh
* flask
* pycurl
* requests
* urllib3 

# How
1. In one terminal, run: python app.py
2. In another terminal, run: python benchmark.py
3. Tests take ~1 minute to finish all of them, then you can close process in terminal 1. 

# Why
To answer the question: does performance differ, for python HTTP clients?
Also to possibly benchmark different platforms for running an application (and Docker networking).

# My results

On an Xubuntu 14.10 box, CPU Intel(R) Core(TM) i5-3210M CPU @ 2.50GHz
Using Python 2.7.8

```
Testing pycurl performance with 10000 cycles
pycurl: ran 10000 HTTP GET requests in 6.2360830307 seconds
Testing pycurl (saving response body by cStringIO) performance with 10000 cycles
pycurl (saving response body by cStringIO): ran 10000 HTTP GET requests in 6.18679094315 seconds
Testing urllib3 performance with 10000 cycles
urllib3: ran 10000 HTTP GET requests in 9.88711500168 seconds
Testing urllib2 performance with 10000 cycles
urllib2: ran 10000 HTTP GET requests in 9.054500103 seconds
Testing urllib performance with 10000 cycles
urllib: ran 10000 HTTP GET requests in 10.8962438107 seconds
Testing 'requests' performance with 10000 cycles
'requests': ran 10000 HTTP GET requests in 21.4645440578 seconds
Testing pycurl (saving response body by cStringIO BUT MAKING A NEW HANDLE EVERY TIME)  performance with 10000 cycles
pycurl (saving response body by cStringIO BUT MAKING A NEW HANDLE EVERY TIME): ran 10000 HTTP GET requests in 6.031294 seconds
Testing pycurl (saving response body by cStringIO)  CONNECTION REUSE performance with 10000 cycles
pycurl (saving response body by cStringIO)  with CONNECTION REUSE: ran 10000 HTTP GET requests in 1.608877 seconds
Testing urllib3 CONNECTION REUSE performance with 10000 cycles
urllib3 with CONNECTION REUSE: ran 10000 HTTP GET requests in 5.654499 seconds
```

**Note that pycurl with Curl handle reuse can do the same work in 1.6 seconds that requests does in 17.90 seconds.**  

# Docker Building It (issues with the base image currently)
```shell
./build-docker.sh
./run-docker.sh
```