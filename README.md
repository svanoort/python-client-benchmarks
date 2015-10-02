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
So you can benchmark different clients... and possibly different platforms for running an application

# My results

On an Xubuntu 14.10 box, CPU Intel(R) Core(TM) i5-3210M CPU @ 2.50GHz
Using Python 2.7.8

Testing pycurl performance with 10000 cycles
pycurl: ran 10000 HTTP GET requests in 5.63378810883 seconds
Testing pycurl (saving response body by cStringIO) performance with 10000 cycles
pycurl (saving request body by cStringIO): ran 10000 HTTP GET requests in 5.61715292931 seconds
Testing urllib3 performance with 10000 cycles
urllib3: ran 10000 HTTP GET requests in 9.55537605286 seconds
Testing urllib2 performance with 10000 cycles
urllib2: ran 10000 HTTP GET requests in 8.73536992073 seconds
Testing urllib performance with 10000 cycles
urllib: ran 10000 HTTP GET requests in 9.98209905624 seconds
Testing 'requests' performance with 10000 cycles
'requests': ran 10000 HTTP GET requests in 17.902536869 seconds
Testing pycurl (saving request body by cStringIO)  CONNECTION REUSE performance with 10000 cycles
**pycurl (saving response body by cStringIO)  with CONNECTION REUSE: ran 10000 HTTP GET requests in 0.010255 seconds** *No, that is not a bug, I verified it's really submitting separate requests.*
Testing urllib3 CONNECTION REUSE performance with 10000 cycles
urllib3 with CONNECTION REUSE: ran 10000 HTTP GET requests in 5.368338 seconds

# Docker Building It (issues with the base image currently)
```shell
./build-docker.sh
./run-docker.sh
```