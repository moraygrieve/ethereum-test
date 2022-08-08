FROM ubuntu:20.04

RUN apt update
RUN apt install python3-pip
RUN python3 -m pip install web3
RUN python3 -m pip install pysys==1.6.1

