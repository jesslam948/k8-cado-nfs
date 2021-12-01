# syntax=docker/dockerfile:1
FROM ubuntu:latest
MAINTAINER jessica lam
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y git make cmake g++ libgmp*-dev python python3 ssh rsync gzip
RUN git clone https://gitlab.inria.fr/cado-nfs/cado-nfs.git
COPY local.sh /cado-nfs/local.sh
RUN cd /cado-nfs/ && make
