# syntax=docker/dockerfile:1
FROM ubuntu:latest as build
MAINTAINER jessica lam
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y git make cmake g++ libgmp*-dev python3 ssh rsync gzip bc locales cmake python3 libhwloc-dev libgmp-dev libecm-dev libfmt-dev
RUN git clone https://gitlab.inria.fr/cado-nfs/cado-nfs.git
COPY local.sh /cado-nfs/local.sh
ENV PREFIX=/usr/local
RUN cd /cado-nfs/ && make cmake
RUN cd /cado-nfs/ && make -j8
RUN cd /cado-nfs/ && make install
COPY dispatch-files.sh /
RUN /dispatch-files.sh
RUN find /usr/local -type f

# syntax=docker/dockerfile:1
FROM ubuntu:latest as runtime
MAINTAINER jessica lam
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y ca-certificates python3 gzip bc libgomp1 libhwloc15 libgmp10

# syntax=docker/dockerfile:1
FROM runtime
MAINTAINER jessica lam
COPY --from=build /usr/local/factoring-server/ /usr/local/
COPY --from=build /usr/local/factoring-client/ /usr/local/
