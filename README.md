# python-client-benchmarks
Simple demonstration of benchmarking different python HTTP client tools with a trivial Flask app (returns 'pong' from http://localhost:5000/ping) running in gUnicorn

# Requirements
(in requirements.txt)

# How
1. In one terminal, build & run the docker image to start a test server: `sh build-docker.sh && sh run-docker.sh`
2. In another terminal, run: python benchmark.py
3. Tests take a few minutes minute to finish, then you can close process in terminal 1. 

# Why
To answer the question: does performance differ, for python HTTP clients?
Also to possibly benchmark different platforms for running an application (and Docker networking).

# My results

On an Xubuntu 14.10 box, CPU Intel(R) Core(TM) i5-3210M CPU @ 2.50GHz
Using Python 2.7.8

```
START testing requests performance with 10000 cycles and connection reuse False
Options: 
END testing result: 26.9634430408
 
START testing requests performance with 10000 cycles and connection reuse True
Options: 
END testing result: 13.2264149189
 
START testing pycurl performance with 10000 cycles and connection reuse True
Options: Reuse handle, don't save body
END testing result: 6.24056100845
 
START testing pycurl performance with 10000 cycles and connection reuse True
Options: Reuse handle, save response to new cStringIO buffer
END testing result: 6.03981900215
 
START testing pycurl performance with 10000 cycles and connection reuse False
Options: Reuse handle, save response to new cStringIO buffer
END testing result: 12.0486500263
 
START testing pycurl performance with 10000 cycles and connection reuse False
Options: New handle, save response to new cStringIO buffer
END testing result: 59.0295059681
 
START testing urllib3 performance with 10000 cycles and connection reuse True
Options: 
END testing result: 9.26859688759
 
START testing urllib2 performance with 10000 cycles and connection reuse False
Options: 
END testing result: 16.1479890347
 
START testing urllib performance with 10000 cycles and connection reuse False
Options: 
END testing result: 17.7717568874
```