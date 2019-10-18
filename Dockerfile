FROM resin/raspberry-pi-python:3

RUN pip install slackbot
RUN pip install picamera

WORKDIR /app
ADD . /app

ENTRYPOINT ["/usr/local/bin/python", "/app/run.py"]