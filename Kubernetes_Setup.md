# How to setup Kubernetes with Ubuntu VMs
## Initial Setup
- Main Node
	- Ubuntu VM
	- 2 cores
	- 2 GB RAM
	- 2nd network adapter; host-only
- Client Nodes
	- Ubuntu VM
	- 1 core
	- 1 GB RAM
	- 2nd network adapter; host-only
## Both Main and Client Nodes
1. Turn off swap space
	- `sudo swapoff -a`
	- edit `/etc/fstab` and comment out the line that mentions swap
2. Update hostnames
	-	edit `/etc/hostname` to be `kmain` or `knode1`, etc. depending on the type
3. Update hosts file with ips
	- edit `/etc/hosts` with the ip addr and hostname of all hosts (main and clients); make sure to use the ip associated with the interface `enp0s8`, which is the host-only adapter
4. Set static ip addrs ([source](https://linuxize.com/post/how-to-configure-static-ip-address-on-ubuntu-20-04/))
	- Ubuntu 17.10+ uses `netplan` instead of `ifconfig`
	- edit `/etc/netplan/*.yaml` (there should be a default file there, just use that) and add to the ethernets part like below
		``` yaml
		  ethernets:
			enp0s8:
			  dhcp4: no
			  addresses:
				  - 192.168.56.101/24
			  gateway4: 192.168.56.100
			  nameservers:
				addresses: [8.8.8.8, 1.1.1.1]
		```
	- apply changes `sudo netplan apply`
	- check with `ip addr show dev enp0s8`
5. Update and install
	``` bash
	apt-get update
	apt-get install -y openssh-server docker.io apt-transport-https curl
	curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
	cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
	deb http://apt.kubernetes.io/ kubernetes-xenial main
	EOF
	apt-get update
	apt-get install -y kubelet kubeadm kubectl

	```
6. Set cgroup driver for docker
	- create file `/etc/docker/daemon.json` and add
		``` json
		{
			"exec-opts": ["native.cgroupdriver=systemd"]
		}
		```
	- as *root*, run the following:
		- `systemctl daemon-reload`
		- `systemctl restart docker`
		- `systemctl start kubelet`

## On the Main Node
1. Start Kubernetes cluster
	- run `sudo kubeadm init --apiserver-advertise-address=192.168.56.101 --pod-network-cidr=192.168.0.0/16`
	- if done successfully save the starting commands (examples below)
		- to start as a regular user:
			``` bash
			mkdir -p $HOME/.kube
			sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
			sudo chown $(id -u):$(id -g) $HOME/.kube/config
			```
		- example to join worker nodes (this will change everytime we init):
			``` bash
			sudo kubeadm join 192.168.56.101:6443 --token 19lwns.xu7w7b6te7dzlv1i --discovery-token-ca-cert-hash sha256:04acbbc2e4f42850b87aae8eefabc27bf363785d85c0ca21b8566b6f318f3bbe 
			```
2. Run the commands for starting as a regular user
3. Verify kubectl works
	- `kubectl get pods -o wide --all-namespaces`
4. Setup networking (get the coredns to work) ([source](https://stackoverflow.com/questions/52609257/coredns-in-pending-state-in-kubernetes-cluster))
	- for CNI plugins to work `sudo sysctl net.bridge.bridge-nf-call-iptables=1`
	- I used [flannel](https://github.com/flannel-io/flannel) for networking `kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml`
		- but we can choose from any in this [list](https://kubernetes.io/docs/concepts/cluster-administration/addons/)
	- flannel wasn't working so I switched to calico:
		- make sure there aren't any other cni configs in /etc/cni/net.d
		- follow these [instructions](https://projectcalico.docs.tigera.io/getting-started/kubernetes/quickstart#install-calico)
		- NOTE: for calico to work, the pod-network-cidr flag must be in use when doing the kubeadm init
## On the Client Nodes
1. Join the worker node
	- `sudo kubeadm join --apiserver-advertise-address=192.168.56.101 --pod-network-cidr=192.168.0.0/16`
2. Check node was joined successfully by running `kubectl get nodes` on the main node