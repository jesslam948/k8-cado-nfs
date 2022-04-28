import subprocess
from datetime import datetime

# Turn off usage reporting, slows down gcloud cli
subprocess.run("gcloud config set disable_usage_reporting True", shell=True)

start_time = datetime.now()
# Create the cluster
cluster_create = subprocess.run("gcloud container clusters create cadonfs-cluster --machine-type=c2-standard-4 --num-nodes=2 --node-labels=stage=polysel", shell=True)
if cluster_create.returncode != 0:
    print("cluster creation failed")
    exit()

# Create persistent disk
disk_create = subprocess.run("gcloud compute disks create --size=10GB --zone=us-central1-a server-pv", shell=True)
if disk_create.returncode != 0:
    print("disk creation failed")
    exit()

# These are needed throughout the program -- the params, service, and storage
subprocess.Popen("kubectl create cm param-cfg --from-file cado_params/params", shell=True)
subprocess.Popen("kubectl create -f yaml_files/gcp2/cadoservice.yml", shell=True)
subprocess.Popen("kubectl create -f yaml_files/gcp2/storage-pv.yml", shell=True)

# Polysel stage
subprocess.run("kubectl create -f yaml_files/gcp2/1polysel.yml", shell=True)
subprocess.run("kubectl wait --for=condition=complete --timeout=10m job/polysel", shell=True)

# Polysel cleanup
subprocess.Popen("kubectl delete jobs polysel", shell=True)

# Sieving stage
subprocess.Popen("gcloud container node-pools create sieve-pool --cluster=cadonfs-cluster --machine-type=e2-standard-4 --num-nodes=2 --node-labels=stage=sieve", shell=True)
subprocess.run("kubectl create -f yaml_files/gcp2/2sieve.yml", shell=True)
subprocess.run("kubectl wait --for=condition=complete --timeout=40m job/sieve", shell=True)

# Sieving cleanup
subprocess.Popen("kubectl delete jobs sieve", shell=True)
subprocess.Popen("kubectl delete deployment polyselclient", shell=True)
subprocess.Popen("kubectl delete deployment sieveclient", shell=True)
subprocess.Popen("gcloud container node-pools delete sieve-pool --cluster=cadonfs-cluster --quiet", shell=True)

# Linalg stage
subprocess.run("kubectl create -f yaml_files/gcp2/3linalg.yml", shell=True)
end_time = datetime.now()

# LinAlg cleanup
subprocess.run("kubectl wait --for=condition=complete --timeout=15m job/linalg", shell=True)
subprocess.Popen("kubectl delete jobs linalg", shell=True)

### EXTRA STEP FOR LOGGING
# Get log files
subprocess.run("kubectl create -f yaml_files/gcp2/4logs.yml", shell=True)
subprocess.run("kubectl cp logs:/tmp ./logs", shell=True)

# Get log files cleanup
subprocess.Popen("kubectl delete pods logs", shell=True)

# Cleanup
subprocess.run("kubectl delete cm param-cfg", shell=True)
subprocess.run("kubectl delete pvc sever-storage-claim", shell=True)
subprocess.run("kubectl delete storageclass server-storage-class", shell=True)
subprocess.run("gcloud compute disks delete server-pv --quiet", shell=True) # the previous line should delete this but just in case!
subprocess.run("gcloud container clusters delete cadonfs-cluster --quiet", shell=True)

print(f"Finished! Start time: {start_time} End time: {end_time} Elapsed time: {end_time - start_time}"