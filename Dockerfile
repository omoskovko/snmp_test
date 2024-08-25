# Build image using this Dockerfile
#    docker build -t my-snmp-image .
#
# Run container using this image:
#   docker run --name my-snmp-container -it -d my-snmp-image
#
# To run tests:
#   docker exec -it my-snmp-container /home/usnmp/snmp_test/run_test.sh

FROM ubuntu:latest
LABEL maintainer="omoskovko@gmail.com"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y snmpd snmp snmp-mibs-downloader python3 python3-pip python3-venv iproute2 iputils-ping net-tools

RUN download-mibs

ARG USER_ID=999
RUN useradd -rm -d /home/usnmp -s /bin/bash -g root -G sudo -u ${USER_ID} usnmp
RUN chown -R usnmp /home/usnmp 
USER usnmp

WORKDIR /home/usnmp
# Copy the requirements file into the container
COPY requirements.txt .

# Switch to Bash as the default shell
SHELL ["/bin/bash", "-c"]

RUN mkdir venv
RUN python3 -m venv ./venv 
RUN source ./venv/bin/activate && python3 -m pip install --upgrade pip
RUN source ./venv/bin/activate && pip3 install --no-cache-dir -r requirements.txt
ENV PATH="/usr/bin:$PATH"

RUN mkdir -p snmp_test
WORKDIR /home/usnmp/snmp_test
RUN umask 0002
COPY . .