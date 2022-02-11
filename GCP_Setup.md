## Setting up Kubernetes with Google Cloud
[source](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app)

### Initial Setup
Before starting:
- Set up a GCP account
- Set up a Cloud project with billing
    - Please read GCP billing info thoroughly & consider setting up a "budget" that will alert you on costs accrued
- Enable the Artifact Registry and Google Kubernetes Engine APIs

Optional:
> I prefer running this in a local shell so this is the required setup if you go this route, otherwise you can just use the Console or the online Cloud Shell
- Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
    - Use the `gcloud auth login` to attach the cli to your account
    - Run `gcloud components install kubectl`
- Install [Docker Community Edition](https://docs.docker.com/engine/install/)
    - Use `docker login` to login to your Docker account

### Setting up the Image in the Artifact Registry
Create a repository
1. Set PROJECT_ID corresponding to your Cloud project
    - `export PROJECT_ID=<project_id>`
2. Set project id for CLI
    - `gcloud config set project $PROJECT_ID`
3. Create the `cado-nfs-repo`
    ``` bash
    gcloud artifacts repositories create cado-nfs-repo --repository-format=docker --location=us-west2 --description="Docker repository"
    ```

Get the Docker Image
1. Pull the Docker image (on directions on how to create your own, check out `Docker_Setup.md`)
    - `docker pull jessica948/cadonfs:latest`

Push the Image to the Registry
1. Set up Docker auth in your region (I use `us-west2`)
    - `gcloud auth configure-docker us-west2-docker.pkg.dev`
2. Tag your image
    - `docker tag jessica948/cadonfs:latest us-west2-docker.pkg.dev/k8-cado-nfs/cado-nfs-repo/cadonfs`
3. Push the image
    - `docker push us-west2-docker.pkg.dev/k8-cado-nfs/cado-nfs-repo/cadonfs`
    - make sure the right docker config is being used (its in your account's home directory, not under root, etc.) otherwise you may be getting permission denied errors

### Setting up with Google Cloud
Create a GKE Cluster
1. For a standard cluster, set your zone
    - `gcloud config set compute/zone us-west2-a`
2. Create the standard cluster
    - `gcloud container clusters create cadonfs-cluster`
    - this will take a while

Run Cado-NFS
1. We can treat it like running kubectl normally (check `Pod_Setup.md`)

Clean up to prevent extra incurred costs
1. Delete pods, services, and deployments
    - `kubectl delete [svc, deployment, pods] [name]`
2. Delete the cluster
    - `gcloud container clusters delete cadonfs-cluster --zone us-west2-a`
4. Clean up the artifact registry
    - `gcloud artifacts docker images delete us-west2-docker.pkg.dev/k8-cado-nfs/cado-nfs-repo/cadonfs:latest --delete-tags`
