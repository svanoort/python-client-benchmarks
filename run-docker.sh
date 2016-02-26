#!/bin/bash
docker run --rm -i -t -w /tmp -p 5000:5000 -p 4443:443 -p 8080:80 client-flask-demo:1.0
