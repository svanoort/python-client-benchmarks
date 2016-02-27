#/usr/bin/env/python
import timeit
import time
import string
import argparse
import csv
import sys

if sys.version_info[0] > 2:
    import urllib.parse as urlparse    
else:
    import urlparse

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

def run_test(library, url, cycles, connection_reuse, options, setup_test, run_test, delay=None):
    """ Runs a benchmark, showing start & stop 
        the setup_test is a String.template with $url as an option
        the run_test allows for the same
    """
    print("START testing {0} performance with {1} cycles and connection reuse {2}".format(library, cycles, connection_reuse))
    print("Options: {0}".format(options))

    run_cmd = string.Template(run_test).substitute(url=url)
    if delay:
        run_cmd = run_cmd + "; time.sleep({0})".format(delay)
    setup_cmd = string.Template(setup_test).substitute(url=url)

    mytime = timeit.timeit(stmt=run_cmd, setup=setup_cmd, number=cycles)
    if delay:
        mytime = mytime - (delay * cycles)

    print("END testing result: {0}".format(mytime))
    print(' ')
    result = [library, connection_reuse, options, cycles, mytime]
    return result

def run_size_benchmarks(url='', cycles=10, delay=None, output_file=None, length_api_format='/length/$length', **kwargs):
    timer_type = kwargs.get('timer')
    TIMER = timeit.default_timer

    if timer_type and timer_type.lower() == 'cpu':
        TIMER = time.clock  # Linux only



    """ Run variable-size benchmarks, where URL is the base url """
    sizes = [4, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]  # Yields ~10 GB of traffic, be careful!

    REQUESTS_NOREUSE = ('requests', False, 'Default', 
        'import requests', 
        "r = requests.get('$url', verify=False)")
    REQUESTS_REUSE = ('requests', True, 'Default', 
        "import requests; \
            session = requests.Session(); \
            r = requests.Request('GET', '$url').prepare()", 
        "v = session.send(r, verify=False)")
    PYCURL_REUSE = ('pycurl', True, "Reuse handle, save response to new cStringIO buffer", 
        "from pycurl import Curl; from cStringIO import StringIO; \
            mycurl=Curl(); \
            mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
            mycurl.setopt(mycurl.SSL_VERIFYHOST, 0); \
            mycurl.setopt(mycurl.URL, '$url')",
        "body = StringIO(); \
            mycurl.setopt(mycurl.WRITEFUNCTION, body.write); \
            mycurl.perform(); \
            val = body.getvalue(); \
            body.close()")
    PYCURL_NOREUSE = ('pycurl', False, "Reuse handle, save response to new cStringIO buffer", 
        "from pycurl import Curl; from cStringIO import StringIO; \
            mycurl=Curl(); \
            mycurl.setopt(mycurl.URL, '$url'); \
            mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
            mycurl.setopt(mycurl.SSL_VERIFYHOST, 0); \
            body = StringIO(); \
            mycurl.setopt(mycurl.FORBID_REUSE, 1)",
        "body = StringIO(); \
            mycurl.setopt(mycurl.WRITEFUNCTION, body.write); \
            mycurl.perform(); \
            val = body.getvalue(); \
            body.close()")

    TEST_TYPES = [REQUESTS_NOREUSE, PYCURL_NOREUSE, REQUESTS_REUSE, PYCURL_REUSE]

    all_results = list()

    # Run tests 
    for size in sizes:
        temp_url = url + string.Template(length_api_format).substitute(length=size)
        for test in TEST_TYPES:
            result = run_test(test[0], temp_url, cycles, test[1], test[2], test[3], test[4], delay=delay)
            del result[3]  # Don't need cycles
            result.insert(0, size)
            all_results.append(result)
    
    # Transform tuples to size, time graphs for each response size
    final_output = [[x, 0, 0, 0, 0] for x in sizes]
    for i in xrange(0, len(sizes)):
        final_output[i][1] = all_results[i*4][4]
        final_output[i][2] = all_results[i*4+1][4]
        final_output[i][3] = all_results[i*4+2][4]
        final_output[i][4] = all_results[i*4+3][4]

    headers = ('Response_size', 'Requests Time (no cnxn reuse)', 'pyCurl Time (no cnxn reuse)',
               'Requests Time (cnxn reuse)', 'pyCurl Time (cnxn reuse)')
    if output_file:
        with open(output_file, 'wb') as csvfile:
            outwriter = csv.writer(csvfile, dialect=csv.excel)
            outwriter.writerow(headers)
            for result in final_output:
                outwriter.writerow(result)

def run_all_benchmarks(url='', cycles=10, delay=None, output_file=None, **kwargs):
    results = list()

    headers = ('Library','Reuse Connections?','Options', 'Time')
    tests = list()

    timer_type = kwargs.get('timer')
    TIMER = timeit.default_timer

    if timer_type and timer_type.lower() == 'cpu':
        TIMER = time.clock  # Linux only

    # Library, cnxn_reuse, options, setup, run_stmt
    # Requests
    tests.append(('requests', False, 'Default', 
        'import requests', 
        "r = requests.get('$url', verify=False)"))
    
    tests.append(('requests', True, 'Default', 
        "import requests; \
            session = requests.Session(); \
            r = requests.Request('GET', '$url').prepare()", 
        "v = session.send(r, verify=False)"))
    
    # PyCurl
    tests.append(('pycurl', True, "Reuse handle, don't save body", 
        "from pycurl import Curl; \
            mycurl=Curl(); \
            mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
            mycurl.setopt(mycurl.SSL_VERIFYHOST, 0); \
            mycurl.setopt(mycurl.URL, '$url'); \
            mycurl.setopt(mycurl.WRITEFUNCTION, lambda x: None)",
        "mycurl.perform()"))

    tests.append(('pycurl', True, "Reuse handle, save response to new cStringIO buffer", 
        "from pycurl import Curl; from cStringIO import StringIO; \
            mycurl=Curl(); \
            mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
            mycurl.setopt(mycurl.SSL_VERIFYHOST, 0); \
            mycurl.setopt(mycurl.URL, '$url')",
        "body = StringIO(); \
            mycurl.setopt(mycurl.WRITEFUNCTION, body.write); \
            mycurl.perform(); \
            val = body.getvalue(); \
            body.close()"))

    tests.append(('pycurl', False, "Reuse handle, save response to new cStringIO buffer", 
        "from pycurl import Curl; from cStringIO import StringIO; \
            mycurl=Curl(); \
            mycurl.setopt(mycurl.URL, '$url'); \
            mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
            mycurl.setopt(mycurl.SSL_VERIFYHOST, 0); \
            body = StringIO(); \
            mycurl.setopt(mycurl.FORBID_REUSE, 1)",
        "body = StringIO(); \
            mycurl.setopt(mycurl.WRITEFUNCTION, body.write); \
            mycurl.perform(); \
            val = body.getvalue(); \
            body.close()"))

    # The use of global DNS cache avoids a bug on some linux systems with libcurl 
    #  playing badly with DNS resolvers
    tests.append(('pycurl', False, "New handle, save response to new cStringIO buffer", 
        "from pycurl import Curl; from cStringIO import StringIO",
        "body = StringIO(); \
            mycurl=Curl(); \
            body = StringIO(); \
            mycurl.setopt(mycurl.URL, '$url'); \
            mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
            mycurl.setopt(mycurl.SSL_VERIFYHOST, 0); \
            mycurl.setopt(mycurl.DNS_USE_GLOBAL_CACHE, True); \
            mycurl.setopt(mycurl.WRITEFUNCTION, body.write); \
            mycurl.perform(); \
            val = body.getvalue(); \
            body.close()"))

    # URLLIB3
    # Making URLLIB3 accept self-signed certs is a beast.  You have to create a connection pool with the hostname and port supplied.
    # See: http://stackoverflow.com/questions/18061640/ignore-certificate-validation-with-urllib3
    # Yes, there's an option to bypass hostname verification but I cannot make it play nicely.
    
    parsed_url = urlparse.urlparse(url)
    scheme = parsed_url.scheme
    hostname = parsed_url.hostname
    port = parsed_url.port
    
    setup_string = ""
    if scheme == 'https':
        setup_string = "import urllib3; \
            http_pool = urllib3.HTTPSConnectionPool('{0}', port={1}, cert_reqs='CERT_NONE', assert_hostname=False)".format(hostname, port)
    else:
        setup_string = "import urllib3; http_pool = urllib3.PoolManager()"

    tests.append(('urllib3', True, 'Default', 
        setup_string,
        "body = http_pool.urlopen('GET', '$url').read()"))
    
    # URLLIB2
    #tests.append(('urllib2', False, '', 
    #    "import urllib2",
    #    "body = urllib2.urlopen('$url').read()"))

    # URLLIB
    tests.append(('urllib', False, 'Default', 
        "import urllib",
        "body = urllib.urlopen('$url').read()"))

    for test in tests:
        my_result = run_test(test[0], url, cycles, test[1], test[2], test[3], test[4], delay=delay)
        results.append((test[0], test[1], test[2], my_result[-1]))

    if output_file:
        with open(output_file, 'wb') as csvfile:
            outwriter = csv.writer(csvfile, dialect=csv.excel)
            outwriter.writerow(('url', 'cycles', 'delay'))
            outwriter.writerow((url, cycles, delay))
            outwriter.writerow(headers)
            for result in results:
                outwriter.writerow(result)

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description="Benchmark different python request frameworks")
    parser.add_argument('--url', metavar='u', type=str, default='http://localhost:8080/ping', help="URL to run requests against")
    parser.add_argument('--cycles', metavar='c', type=int, default=10000, help="Number of cycles to run")    
    parser.add_argument('--delay', metavar='d', type=float, help="Delay in seconds between requests")    
    parser.add_argument('--output-file', metavar='o', nargs='?', type=str, help="Output file to write CSV results to")
    parser.add_argument('--benchmark-type', type=str, default="full", choices=('full','size'), help="Benchmark type to run:  full [default]=all libraries, 1 request, size=basic pycurl/requests tests with different request sizes")
    parser.add_argument('--timer', type=str, default="real", choices=('real','cpu'), help="Timer type: real [default] or cpu")
    parser.add_argument('--length-api-format', metavar='l', type=str, default="/length/$length", help="Template for API request that accepts response length parameter, for size benchmarks")
    args = vars(parser.parse_args())
    if args.get('url') is None:
        print("No URL supplied, you must supply a URL!")
        exit(1)
    print('RUNNING PYTHON CLIENT BENCHMARKS WITH ARGS: {0}'.format(args))
    
    if args['benchmark_type'] == 'full':
        run_all_benchmarks(**args)
    elif args['benchmark_type'] =='size':
        run_size_benchmarks(**args)
    else:
        raise Exception("Illegal benchmark type: {0}".format(args['benchmark_type']))

    
