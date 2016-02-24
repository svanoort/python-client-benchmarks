#/usr/bin/env/python
import timeit
import time
import string
import argparse

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

def run_test(library, url, cycles, connection_reuse, options, setup_test, run_test, delay=0.05):
    """ Runs a benchmark, showing start & stop 
        the setup_test is a String.template with $url as an option
        the run_test allows for the same
    """
    print("START testing {0} performance with {1} cycles and connection reuse {2}".format(library, cycles, connection_reuse))
    print("Options: {0}".format(options))
    mytime = timeit.timeit(stmt=string.Template(run_test).substitute(url=url)+"; time.sleep({0})".format(delay),
        setup=string.Template(setup_test).substitute(url=url), 
        number=cycles)
    mytime = mytime - (delay * cycles)
    print("END testing result: {0}".format(mytime))
    result = (library, connection_reuse, options, cycles, mytime)
    return result

def run_all_benchmarks(url='', cycles=10, delay=0.05, **kwargs):
    results = list()

    headers = ('Library','Reuse Connections?','Options', 'Time')
    tests = list()

    # Library, cnxn_reuse, options, setup, run_stmt
    # Requests
    tests.append(('requests', False, '', 
        'import requests', 
        "r = requests.get('$url')"))
    
    tests.append(('requests', True, '', 
        "import requests; \
            session = requests.Session(); \
            r = requests.Request('GET', '$url').prepare()", 
        "v = session.send(r)"))
    
    # PyCurl
    tests.append(('pycurl', True, "Reuse handle, don't save body", 
        "from pycurl import Curl; \
            mycurl=Curl(); \
            mycurl.setopt(mycurl.URL, '$url'); \
            mycurl.setopt(mycurl.WRITEFUNCTION, lambda x: None)",
        "mycurl.perform()"))

    tests.append(('pycurl', True, "Reuse handle, save response to new cStringIO buffer", 
        "from pycurl import Curl; from cStringIO import StringIO; \
            mycurl=Curl(); \
            mycurl.setopt(mycurl.URL, '$url')",
        "body = StringIO(); \
            mycurl.setopt(mycurl.WRITEDATA, body); \
            mycurl.perform(); \
            val = body.getvalue(); \
            body.close()"))

    tests.append(('pycurl', False, "Reuse handle, save response to new cStringIO buffer", 
        "from pycurl import Curl; from cStringIO import StringIO; \
            mycurl=Curl(); \
            mycurl.setopt(mycurl.URL, '$url'); \
            body = StringIO(); \
            mycurl.setopt(mycurl.FORBID_REUSE, 1)",
        "body = StringIO(); \
            mycurl.setopt(mycurl.WRITEDATA, body); \
            mycurl.perform(); \
            val = body.getvalue(); \
            body.close()"))

    tests.append(('pycurl', False, "New handle, save response to new cStringIO buffer", 
        "from pycurl import Curl; from cStringIO import StringIO",
        "body = StringIO(); \
            mycurl=Curl(); \
            body = StringIO(); \
            mycurl.setopt(mycurl.URL, '$url'); \
            mycurl.setopt(mycurl.WRITEDATA, body); \
            mycurl.perform(); \
            val = body.getvalue(); \
            body.close()"))

    # URLLIB3
    tests.append(('urllib3', True, '', 
        "import urllib3; http_pool = urllib3.PoolManager()",
        "body = http_pool.urlopen('GET', '$url').read()"))
    
    # URLLIB2
    tests.append(('urllib2', False, '', 
        "import urllib2",
        "body = urllib2.urlopen('$url').read()"))

    # URLLIB
    tests.append(('urllib', False, '', 
        "import urllib",
        "body = urllib.urlopen('$url').read()"))

    for test in tests:
        my_result = run_test(test[0], url, cycles, test[1], test[2], test[3], test[4], delay=delay)
        results.append((test[0], test[1], test[2], my_result))

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description="Benchmark different python request frameworks")
    parser.add_argument('--url', metavar='u', type=str, default='http://localhost:5000/ping', help="URL to run requests against")
    parser.add_argument('--cycles', metavar='c', type=int, default=1000, help="Number of cycles to run")    
    parser.add_argument('--delay', metavar='d', type=float, default=0.05, help="Delay in seconds between requests")    
    parser.add_argument('--output-file', metavar='o', type=str, help="Output file to write CSV results to")
    args = vars(parser.parse_args())
    if args.get('url') is None:
        print("No URL supplied, you must supply a URL!")
        exit(1)
    print args
    run_all_benchmarks(**args)
