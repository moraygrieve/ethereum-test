FROM --platform=linux/amd64 ubuntu:20.04

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:ethereum/ethereum
RUN apt update
RUN apt install -y solc

RUN apt install -y vim
RUN apt install -y python3-pip
RUN python3 -m pip install web3
RUN python3 -m pip install pysys==1.6.1
RUN python3 -m pip install py-solc-x

RUN mkdir /home/obscuro-test
COPY . /home/obscuro-test

