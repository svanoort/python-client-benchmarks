FROM python:2.7.10
MAINTAINER samvanoort@gmail.com
# Install PyCurl via package manager because the native library can be a problem
RUN apt-get update && apt-get install -y python-pycurl && \
	apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
ADD app.py /tmp/
ADD start.sh /tmp/
EXPOSE 5000
CMD /tmp/start.sh
