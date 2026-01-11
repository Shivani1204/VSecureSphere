## KUBERNETES SINGLE NODE CLUSTER SETUP
USING CONTAINERD + FLANNEL WITH SWAP ENABLED
UBUNTU 24.04 LTS

==================================================

## SYSTEM DETAILS

OS                : Ubuntu 24.04.3 LTS (Noble Numbat)
Kubernetes        : v1.33.7
Container Runtime : containerd
CNI               : Flannel
Cgroup            : v2
Node Type          : Single node (control-plane + worker)
Swap               : Enabled (shared / college server)

==================================================

## STEP 1: VERIFY OPERATING SYSTEM

Command:
```
cat /etc/os-release
```

Ensure OS is Ubuntu 24.04 LTS.

==================================================

## STEP 2: SYSTEM PREPARATION

2.1 Load required kernel modules

Commands:
```
sudo modprobe overlay
sudo modprobe br_netfilter
```

Persist modules:
```
sudo tee /etc/modules-load.d/k8s.conf <<EOF
overlay
br_netfilter
EOF
```
---

2.2 Configure sysctl for Kubernetes networking

Command:
```
sudo tee /etc/sysctl.d/k8s.conf <<EOF
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
```

Apply settings:

```
sudo sysctl --system
```

==================================================

## STEP 3: FIREWALL CONFIGURATION (IPTABLES)

Commands:
```
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

sudo iptables -A INPUT -p tcp --dport 6443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 2379:2380 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 10250 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 8472 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 30000:32767 -j ACCEPT
```

Note:
Rules are runtime-only and safe for shared servers.

==================================================

## STEP 4: INSTALL CONTAINERD

Command:
```
sudo apt update
sudo apt install -y containerd
```

Generate default config:
```
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml
```
Edit config:
```
sudo nano /etc/containerd/config.toml
```
Change:
```
SystemdCgroup = false
```
To:
```
SystemdCgroup = true
```

Restart containerd:
```
sudo systemctl restart containerd
sudo systemctl enable containerd
```

Verify:
```
systemctl status containerd
```

==================================================

## STEP 5: INSTALL KUBERNETES COMPONENTS

Install dependencies:
```
sudo apt install -y apt-transport-https ca-certificates curl
```

Add Kubernetes repository:
```
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | \
sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg


echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] \
https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /" | \
sudo tee /etc/apt/sources.list.d/kubernetes.list
```

Install tools:
```
sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```
==================================================

## STEP 6: CREATE KUBEADM CONFIG FILE (REQUIRED FOR SWAP)

Create file:
```
nano kubeadm-config.yaml
```

Paste EXACTLY:

```
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
nodeRegistration:
criSocket: unix:///run/containerd/containerd.sock
kubeletExtraArgs:
fail-swap-on: "false"

---

apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: v1.33.7
networking:
podSubnet: 10.244.0.0/16

---

apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
failSwapOn: false
memorySwap:
swapBehavior: LimitedSwap
```

Save and exit.

==================================================

## STEP 7: INITIALIZE KUBERNETES CLUSTER

Command:
```
sudo kubeadm init --config kubeadm-config.yaml
```

Expected message:
Your Kubernetes control-plane has initialized successfully!

==================================================

## STEP 8: CONFIGURE KUBECTL

Commands:
```
mkdir -p $HOME/.kube
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Verify:
```
kubectl get nodes
```
==================================================

## STEP 9: INSTALL FLANNEL (CNI)

Command:
```
kubectl apply -f [https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml](https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml)
```

Verify:
```
kubectl get pods -n kube-flannel
```
==================================================

## STEP 10: ALLOW WORKLOADS ON CONTROL PLANE

Command:
```
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
```
==================================================

## STEP 11: FINAL VERIFICATION

Commands:
```
kubectl get nodes
kubectl get pods -A
```
Expected Output:
Node status should be READY.

==================================================

## IMPORTANT NOTES

* Swap was NOT disabled due to shared/college server restrictions
* kubeadm configuration file is mandatory when running Kubernetes with swap ON
* containerd is the officially supported runtime for Ubuntu 24.04
* kubelet config is generated by kubeadm during init

==================================================

## CONCLUSION

A fully functional single-node Kubernetes cluster was successfully deployed
on Ubuntu 24.04 using containerd, Flannel, and swap enabled.
This setup is suitable for academic, lab, and shared-server environments.


