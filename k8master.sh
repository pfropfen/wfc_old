#!/bin/bash
sudo apt install docker.io -y
sudo swapoff -a
sudo sed -i '/swap/s/^/#/' /etc/fstab
sudo swapon --show
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ipforward = 1
EOF

sudo sysctl --system
sudo apt install curl ca-certificates apt-transport-https -y
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor
     -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg
sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] 
     https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | 
     sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install kubelet kubeadm kubectl -y

sudo mkdir /etc/containerd
sudo sh -c "containerd config default > /etc/containerd/config.toml"
sudo sed -i 's/ SystemdCgroup = false/ SystemdCgroup = true/' /etc/containerd/config.toml
sudo systemctl restart containerd.service
sudo systemctl restart kubelet.service
sudo systemctl enable kubelet.service

#MASTER PART
sudo kubeadm config images pull
sudo kubeadm init --pod-network-cidr=10.10.0.0/16 > token.sh
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/\
                  manifests/tigera-operator.yaml --validate=false
curl https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/\
     custom-resources.yaml -O
ls -l
sed -i 's/cidr: 192\.168\.0\.0\/16/cidr: 10.10.0.0\/16/g' custom-resources.yaml
kubectl create -f custom-resources.yaml --validate=false
sudo tail -n 2 token.sh > jointoken.sh



