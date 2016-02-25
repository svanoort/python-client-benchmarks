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
{'url': 'http://127.0.0.1:5000/length/10000', 'delay': None, 'cycles': 10000, 'output_file': None}
START testing requests performance with 10000 cycles and connection reuse False
Options: 
END testing result: 22.4408450127
 
START testing requests performance with 10000 cycles and connection reuse True
Options: 
END testing result: 11.0733878613
 
START testing pycurl performance with 10000 cycles and connection reuse True
Options: Reuse handle, don't save body
END testing result: 4.75980710983
 
START testing pycurl performance with 10000 cycles and connection reuse True
Options: Reuse handle, save response to new cStringIO buffer
END testing result: 5.14035511017
 
START testing pycurl performance with 10000 cycles and connection reuse False
Options: Reuse handle, save response to new cStringIO buffer
END testing result: 8.09198617935
 
START testing pycurl performance with 10000 cycles and connection reuse False
Options: New handle, save response to new cStringIO buffer
END testing result: 8.29376411438
 
START testing urllib3 performance with 10000 cycles and connection reuse True
Options: 
END testing result: 7.5977909565
 
START testing urllib2 performance with 10000 cycles and connection reuse False
Options: 
END testing result: 11.6811139584
 
START testing urllib performance with 10000 cycles and connection reuse False
Options: 
END testing result: 13.2057569027
```

Libraries for the local system:
pycurl==7.21.5
requests==2.2.1
urllib3==1.7.1