#!/bin/bash

# create initial cluster with 2 compute optimized machines (4 cores each)
gcloud container clusters create cadonfs-cluster --machine-type=c2-standard-4 --num-nodes=2
# add storage persistent volume
gcloud compute disks create --size=10GB --zone=us-central1-a server-pv

# initial setup with params & service & storage
kubectl create cm param-cfg --from-file cado_params/params
kubectl create -f yaml_files/gcp2/cadoservice.yml
kubectl create -f yaml_files/gcp2/storage-pv.yml

# poly selection stage
kubectl create -f yaml_files/gcp2/1polysel.yml

# remove pod once the job has completed
kubectl delete jobs polysel

# add 2 e2-standard-4 machines (4 cores each) -- new node pool must finish before new pods can use them!!
gcloud container node-pools create sieve-pool --cluster=cadonfs-cluster --machine-type=e2-standard-4 --num-nodes=2

# sieving stage
kubectl create -f yaml_files/gcp2/2sieve.yml

# remove pod once the job has completed
kubectl delete jobs sieve

# remove extra sieving clients
kubectl delete deployment sieveclient

# remove extra nodes 
gcloud container node-pools delete sieve-pool

# linear algebra stage
kubectl create -f yaml_files/gcp2/3linalg.yml


## linux
# gcloud container clusters create cadonfs-cluster --machine-type=c2-standard-4 --num-nodes=2 \
#     && gcloud compute disks create --size=10GB --zone=us-central1-a server-pv \
#     && kubectl create cm param-cfg --from-file cado_params/params \
#     && kubectl create -f yaml_files/gcp2/cadoservice.yml \
#     && kubectl create -f yaml_files/gcp2/storage-pv.yml \
#     && kubectl create -f yaml_files/gcp2/1polysel.yml \
#     && kubectl wait for=condition=complete --timeout=10m job/polysel && kubectl delete jobs polysel \
#     && gcloud container node-pools create sieve-pool --cluster=cadonfs-cluster --machine-type=e2-standard-4 --num-nodes=2 \
#     && kubectl create -f yaml_files/gcp2/2sieve.yml \
#     && kubectl wait for=condition=complete --timeout=40m job/sieve \
#     && kubectl delete jobs sieve \
#     && kubectl delete deployment sieveclient \
#     && gcloud container node-pools delete sieve-pool \
#     && kubectl create -f yaml_files/gcp2/3linalg.yml

## windows :')
gcloud container clusters create cadonfs-cluster --machine-type=c2-standard-4 --num-nodes=2 ^
    && gcloud compute disks create --size=10GB --zone=us-central1-a server-pv ^
    && kubectl create cm param-cfg --from-file cado_params/params ^
    && kubectl create -f yaml_files/gcp2/cadoservice.yml ^
    && kubectl create -f yaml_files/gcp2/storage-pv.yml ^
    && kubectl create -f yaml_files/gcp2/1polysel.yml ^
    && kubectl wait --for=condition=complete --timeout=10m job/polysel ^
    && kubectl delete jobs polysel ^
    && gcloud container node-pools create sieve-pool --cluster=cadonfs-cluster --machine-type=e2-standard-4 --num-nodes=2 ^
    && kubectl create -f yaml_files/gcp2/2sieve.yml ^
    && kubectl wait --for=condition=complete --timeout=40m job/sieve ^
    && kubectl delete jobs sieve ^
    && kubectl delete deployment polyselclient ^
    && kubectl delete deployment sieveclient ^
    && gcloud container node-pools delete sieve-pool --cluster=cadonfs-cluster --quiet ^
    && kubectl create -f yaml_files/gcp2/3linalg.yml


kubectl delete cm param-cfg ^
    && kubectl delete pvc server-storage-claim ^
    && kubectl delete storageclass server-storage-class ^
    && gcloud container node-pools delete sieve-pool --quiet ^
    && gcloud container clusters delete cadonfs-cluster --quiet