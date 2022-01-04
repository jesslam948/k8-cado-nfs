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
5. Check that the pod completed correctly
### Test Two Pods each with One Container
> There will be two pods, one with a container that is the "server" and the other that has a container that is the "client"
1. Make sure that there is a parameter file and a configmap has been created for it (as instructed above)
2. Create two yaml config files (cadotest3s.yml and cadotest3c.yml)
3. Create a service to expose a hostname for the server to the clients (cadoservice.yml)
4. Start the service
5. Create the server pod first (s) and then the client pod (c)
6. Check that the pods completed correctly
### Test One Pod and One Deployment
> There will be one pod with a "server" container and there will be one deployment with multiple (3 in this case) pods that each have a "client" container
1. Make sure that there is a parameter file and cm has been created for it
2. Create the deployment yaml config file (cadotest4c.yml) (we can reuse cadotest3s.yml)
3. Re-use the cadoservice.yml
4. Start the service
5. Start the server pod
6. Start the deployment
7. Check that the factorization completed