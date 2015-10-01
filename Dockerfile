FROM python:2.7.10-slim
MAINTAINER samvanoort@gmail.com
RUN pip install flask
ADD app.py /tmp/
EXPOSE 5000
CMD python /tmp/app.py
