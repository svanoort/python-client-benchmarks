#/usr/bin/env/python
import timeit
import time

# Import clients, so script fails fast if not available
from pycurl import Curl
try:
    from cStringIO import StringIO
except:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
import requests, urllib, urllib2, urllib3

CYCLES = 10000
URL='http://localhost:5000/ping'

# About 6 seconds
LIBRARY="pycurl"
print ("Testing {0} performance with {1} cycles".format(LIBRARY, CYCLES))
mytime = timeit.timeit("mycurl.perform()",
    setup="from pycurl import Curl; \
      mycurl=Curl(); \
      mycurl.setopt(mycurl.URL, '{0}'); \
      mycurl.setopt(mycurl.WRITEFUNCTION, lambda x: None);".format(URL), number=CYCLES)
print('{0}: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, mytime))
print('')

# About 6 sec
LIBRARY="pycurl (saving response body by cStringIO)"
print ("Testing {0} performance with {1} cycles".format(LIBRARY, CYCLES))
mytime = timeit.timeit("mycurl.perform();",
    setup="from pycurl import Curl; from cStringIO import StringIO; \
      mycurl=Curl(); \
      mycurl.setopt(mycurl.URL, '{0}'); \
      body = StringIO(); \
      mycurl.setopt(mycurl.WRITEDATA, body);".format(URL), number=CYCLES)
print('{0}: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, mytime))
print('')

# 10ish seconds
LIBRARY="urllib3"
print ("Testing {0} performance with {1} cycles".format(LIBRARY, CYCLES))
mytime = timeit.timeit("body = http.urlopen('GET', '{0}').read()".format(URL), setup='import urllib3; http=urllib3.PoolManager()', number=CYCLES)
print('{0}: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, mytime))
print('')


# 9ish seconds
LIBRARY="urllib2"
print ("Testing {0} performance with {1} cycles".format(LIBRARY, CYCLES))
mytime = timeit.timeit("body = urllib2.urlopen('{0}').read()".format(URL), setup='import urllib2', number=CYCLES)
print('{0}: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, mytime))
print('')

# 10ish seconds
LIBRARY="urllib"
print ("Testing {0} performance with {1} cycles".format(LIBRARY, CYCLES))
mytime = timeit.timeit("body = urllib.urlopen('{0}').read()".format(URL), setup='import urllib', number=CYCLES)
print('{0}: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, mytime))
print('')

# About 18 seconds?
LIBRARY="'requests'"
print ("Testing {0} performance with {1} cycles".format(LIBRARY, CYCLES))
mytime = timeit.timeit("r = requests.get('{0}')".format(URL), setup='import requests', number=CYCLES)
print('{0}: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, mytime))
print('')

###  CONNECTION REUSE TESTS FOLLOW ###

LIBRARY="pycurl (saving response body by cStringIO BUT MAKING A NEW HANDLE EVERY TIME) "
print ("Testing {0} performance with {1} cycles".format(LIBRARY, CYCLES))
start = time.clock()
for i in xrange(1, CYCLES):
    mycurl=Curl();
    mycurl.setopt(mycurl.URL, URL)
    body = StringIO();
    mycurl.setopt(mycurl.WRITEDATA, body)
    mycurl.perform()
    output = body.getvalue()
    body.close()
    mycurl.close()
end = time.clock()

print('{0}: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, (end-start)))
print('')


LIBRARY="pycurl (saving response body by cStringIO) "
print ("Testing {0} CONNECTION REUSE performance with {1} cycles".format(LIBRARY, CYCLES))
mycurl=Curl();
mycurl.setopt(mycurl.URL, URL)

start = time.clock()
for i in xrange(1, CYCLES):
    body = StringIO();
    mycurl.setopt(mycurl.WRITEDATA, body)
    mycurl.perform()
    output = body.getvalue()
    body.close()
end = time.clock()

print('{0} with CONNECTION REUSE: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, (end-start)))
print('')


LIBRARY="urllib3"
print ("Testing {0} CONNECTION REUSE performance with {1} cycles".format(LIBRARY, CYCLES))
http_pool = urllib3.PoolManager()

start = time.clock()
for i in xrange(1, CYCLES):
    body = http_pool.urlopen('GET', URL).read()
end = time.clock()

print('{0} with CONNECTION REUSE: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, (end-start)))
print('')


LIBRARY="'requests'"
print ("Testing {0} CONNECTION REUSE performance with {1} cycles".format(LIBRARY, CYCLES))
session = requests.Session()

r = requests.Request('GET', URL).prepare()


start = time.clock()
for i in xrange(1, CYCLES):
    session.send(r)
end = time.clock()

print('{0} with CONNECTION REUSE: ran {1} HTTP GET requests in {2} seconds'.format(LIBRARY, CYCLES, (end-start)))
print('')



