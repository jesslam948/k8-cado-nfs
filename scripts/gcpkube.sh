#!/bin/bash
kubectl create cm param-cfg --from-file cado_params/params
kubectl create -f yaml_files/gcp/cadoservice.yml
kubectl create -f yaml_files/gcp/server.yml
kubectl create -f yaml_files/gcp/clients.yml
