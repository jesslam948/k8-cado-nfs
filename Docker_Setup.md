## Creating Your Own Docker Image
If you don't need to create your own image and will be using one that's already publicly available, just pull it using `docker pull [image_name]:[tag]`.
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