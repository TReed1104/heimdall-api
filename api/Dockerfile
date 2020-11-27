## Build from Ubuntu 16.04 base image
FROM ubuntu:16.04

## Disable Interaction
ENV DEBIAN_FRONTEND noninteractive

## Update the image
RUN apt-get clean && \
    apt-get update -y && \
    apt-get upgrade -y

## Install our dependencies
RUN apt-get install python3-pip -y && \
    apt-get install libmysqlclient-dev -y

## Change Working Directory
WORKDIR /usr/src/app

## Install the requirement Python3 modules
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r ./requirements.txt

## Copy the Flask App source files
COPY ./shared.py ./main.py ./scripts/boot.sh ./
COPY ./configs/main.cfg ./configs/main.cfg
COPY ./models ./models
COPY ./resources ./resources

## Give the boot script run permissions
RUN chmod +x ./boot.sh

## Set out exposed port
EXPOSE 5000

## Run out boot script
ENTRYPOINT ["./boot.sh"]
