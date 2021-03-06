import subprocess
import time

processes = []
# # Turn off usage reporting, slows down gcloud cli
# subprocess.run("gcloud config set disable_usage_reporting True", shell=True)

# # Create the cluster with spot nodes automatically
# cluster_create = subprocess.run("gcloud container clusters create cadonfs-cluster --machine-type=c2d-highcpu-16 --num-nodes=4 --node-labels=type=client --spot", shell=True)
# if cluster_create.returncode != 0:
#     print("cluster creation failed")
#     exit()

# # Add a singular node that is non-spot for the server
# processes.append(subprocess.Popen("gcloud container node-pools create server-pool --cluster=cadonfs-cluster --machine-type=c2d-highcpu-4 --num-nodes=1 --node-labels=type=server", shell=True))

# # Create persistent disk
# disk_create = subprocess.run("gcloud compute disks create --size=10GB --zone=us-central1-a server-pv", shell=True)
# if disk_create.returncode != 0:
#     print("disk creation failed")
#     exit()

# # These are needed throughout the program -- the params, service, and storage
# processes.append(subprocess.Popen("kubectl create cm param-cfg --from-file cado_params/params", shell=True))
# processes.append(subprocess.Popen("kubectl create -f yaml_files/gcp2/cadoservice.yml", shell=True))
# processes.append(subprocess.Popen("kubectl create -f yaml_files/gcp2/storage-pv.yml", shell=True))

# # Polysel stage -- creates a polysel server and all of the clients
# subprocess.run("kubectl create -f yaml_files/gcp2/1polysel.yml", shell=True)
# polysel_wait = subprocess.run("kubectl wait --for=condition=complete --timeout=40m job/polysel", shell=True)
# if polysel_wait.returncode != 0:
#     print("waited too long for polynomial selection")
#     exit()

# # Polysel cleanup
# processes.append(subprocess.Popen("kubectl delete jobs polysel", shell=True))

# # Sieving stage
# subprocess.run("kubectl create -f yaml_files/gcp2/2sieve.yml", shell=True)
# sieve_wait = subprocess.run("kubectl wait --for=condition=complete --timeout=120m job/sieve", shell=True)
# if sieve_wait.returncode != 0:
#     print("waited too long for sieving")
#     exit()

# # Sieving cleanup
# processes.append(subprocess.Popen("kubectl delete jobs sieve", shell=True))
# processes.append(subprocess.Popen("kubectl delete deployment cadonfs-client", shell=True))

# # Linalg stage
# subprocess.run("kubectl create -f yaml_files/gcp2/3linalg.yml", shell=True)
# linalg_wait = subprocess.run("kubectl wait --for=condition=complete --timeout=30m job/linalg", shell=True)
# if linalg_wait.returncode != 0:
#     print("waited too long for linear algebra")
#     exit()

# # LinAlg cleanup
# processes.append(subprocess.Popen("kubectl delete jobs linalg", shell=True))

### EXTRA STEP FOR LOGGING
# TODO: find a way to do this more efficiently because, currently, we try to copy before the logs container finishes creating
#   ideally, we would not create a new container for this but somehow get the name of the linalg pod as a variable and cp the logs directly from it
# Get log files
# subprocess.run("kubectl create -f yaml_files/gcp2/4logs.yml", shell=True)
log_collection = subprocess.run("kubectl cp logs:/tmp ./logs", shell=True)
if log_collection.returncode != 0:
    time.sleep(15)
    log_collection = subprocess.run("kubectl cp logs:/tmp ./logs", shell=True)
    if log_collection.returncode != 0:
        print("log collection failed")
        exit()

# Comment out for some troubleshooting
# Get log files cleanup
processes.append(subprocess.Popen("kubectl delete pods logs", shell=True))

# Cleanup
subprocess.run("kubectl delete cm param-cfg", shell=True)
subprocess.run("kubectl delete pvc server-storage-claim", shell=True)
subprocess.run("kubectl delete storageclass server-storage-class", shell=True)
subprocess.run("gcloud compute disks delete server-pv --quiet", shell=True) # the previous line should delete this but just in case!
subprocess.run("gcloud container clusters delete cadonfs-cluster --quiet", shell=True)

# TODO: ? unsure on quite how to do this
for p in processes:
    p.wait()

print(f"Finished!")
