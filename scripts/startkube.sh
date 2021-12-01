#!/bin/bash
# one stop shop for kubeadm init
sudo kubeadm init --apiserver-advertise-address=192.168.56.101 --pod-network-cidr=192.168.0.0/16 
mkdir -p /home/jessicalam/.kube
sudo cp -i /etc/kubernetes/admin.conf /home/jessicalam/.kube/config
sudo chown $(id -u):$(id -g) /home/jessicalam/.kube/config
echo "---DONE---"
