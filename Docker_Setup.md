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
	- create the file named `Dockerfile` (sample can be found in the docker_cado folder)
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
### Test Pod with One Container
> This pod just has one container that does a basic factorization
1. Create the yaml config file (cadotest1.yml)
2. Create the pod
    - run `kubectl create -f cadotest1.yml`
3. Check up on the status of the pod with these commands
    - `kubectl get pods`
    - `kubectl describe pods [nameofpod]`
    - `kubectl logs [nameofpod]`
### Test Pod with Two Containers
> This pod will have two containers, one that is the "server" and one that is a "client"
1. Create a parameter file (examples can be found in the cado-nfs git repo, an example is also provided in the cado_params directory of this repo)
2. Create a configmap for it (so that we can transfer that data to the pod at init)
	- run `kubectl create configmap param-cfg-1 --from-file ~/Desktop/k8-cado-nfs/cado_params/params1`
	- check with `kubectl describe configmaps param-cfg-1`
3. Create the yaml config file (cadotest2.yml)
4. Create the pod
