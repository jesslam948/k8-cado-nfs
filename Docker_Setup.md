## Creating Your Own Docker Image
1. Add yourself to the docker group [source](https://docs.docker.com/engine/install/linux-postinstall/)
	- `sudo groupadd docker`
	- `sudo usermod -aG docker $USER`
	- `newgrp docker` OR log out and log back in
2. Figure out what you need for your application
	- choose a base docker image and create one to figure out what needs to be added on top
		- create the base `sudo docker run --name cadonfs-test -dit -p 80:80 ubuntu`
		- open with bash `sudo docker exec -it cadonfs-test /bin/bash`
	- inside the container, figure out `cado-nfs` specifications
		- `apt-get update`
		- `apt-get install git make cmake g++ libgmp*-dev python python3 ssh rsync gzip`
		- `git clone https://gitlab.inria.fr/cado-nfs/cado-nfs.git`
		- `cd /cado-nfs/`
		- `make`
3. Create the Dockerfile
	- create a new directory to store the file
	- create the file named `Dockerfile`
	- add the following:
		```Dockerfile
		# syntax=docker/dockerfile:1
		FROM ubuntu:latest
		MAINTAINER jessica lam
		ARG DEBIAN_FRONTEND=noninteractive
		RUN apt-get update
		RUN apt-get install -y git make cmake g++ libgmp*-dev python python3 ssh rsync gzip
		RUN git clone https://gitlab.inria.fr/cado-nfs/cado-nfs.git
		RUN cd /cado-nfs/ && make
		```
	- run `docker build -t cadonfs .`
		- the `-t` flag allows us to give the image a name
		- run `docker images` to double check your image is there
4. Setup with private registry ([source](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/))
	- run `docker login` and log into your dockerhub account
	- setup secrets
		``` bash
		kubectl create secret generic regcred --from-file=.dockerconfigjson=<path/to/.docker/config.json> --type=kubernetes.io/dockerconfigjson`
		```
	- tag `docker tag cadonfs jessica948/cadonfs`
	- push `docker push jessica948/cadonfs`
## Creating a Pod
[source](https://medium.com/swlh/how-to-run-locally-built-docker-images-in-kubernetes-b28fbc32cc1d)
1. Create the yaml config file
2. Create the pod
    - run `kubectl create -f cadotemp.yml`
3. Check up on the status of the pod with these commands
    - `kubectl get pods`
    - `kubectl describe pods [nameofpod]`
    - `kubectl logs [nameofpod]`