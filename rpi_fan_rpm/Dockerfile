FROM ghcr.io/home-assistant/amd64-base:3.19

RUN apk add --no-cache python3 py3-pip
RUN pip install pigpio paho-mqtt

COPY run.sh /
COPY rpm.py /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
