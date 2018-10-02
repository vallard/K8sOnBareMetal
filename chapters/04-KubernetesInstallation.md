# Installing Kubernetes


There are many options to install Kubernetes.  We're going to use [kubeadm](https://kubernetes.io/docs/setup/independent/install-kubeadm/)




Install a few dependencies: 

```
for i in $(seq 3); do ssh -t kubec-master-0$i sudo apt-get install -y apt-transport-https curl; done
for i in $(seq 4); do ssh -t kubec0$i sudo apt-get install -y apt-transport-https curl; done
```

Install the apt gpg code.  Here we find that if we are behind a proxy then we will run into issues running ```curl```.  

```
for i in $(seq 3); do ssh -t kubec-master-0$i "https_proxy=proxy.esl.cisco.com:80 curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -"; done
for i in $(seq 4); do ssh -t kubec0$i "https_proxy=proxy.esl.cisco.com:80 curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -"; done
```

Add the repository:

```
for i in $(seq 3); do ssh kubec-master-0$i "sudo echo 'deb http://apt.kubernetes.io/ kubernetes-xenial main' | sudo tee /etc/apt/sources.list.d/kubernetes.list"; done
for i in $(seq 4); do ssh kubec0$i "sudo echo 'deb http://apt.kubernetes.io/ kubernetes-xenial main' | sudo tee /etc/apt/sources.list.d/kubernetes.list"; done
```

Install the packages.  

```
for i in $(seq 3); do ssh -t kubec-master-0$i "sudo apt update && sudo apt install -y kubelet kubeadm kubectl"; done
for i in $(seq 4); do ssh -t kubec0$i "sudo apt update && sudo apt install -y kubelet kubeadm kubectl"; done
```

If you have issues with this command then you may need to add a proxy or check your proxy settings. 

Check that the packages are installed: 

```
for i in $(seq 3); do echo $i; ssh kubec-master-0$i which kubectl; done
```

Now put them on hold so that they aren't automatically updated.  

```
for i in $(seq 3); do ssh kubec-master-0$i sudo apt-mark hold kubelet kubeadm kubectl; done
for i in $(seq 3); do ssh kubec0$i sudo apt-mark hold kubelet kubeadm kubectl; done
```


## Load Balancer

We would like to make our master nodes redundant but we can't do that without a load balancer, or VIP.  There are several options here: 

1.  We could go with an external load balancer like a Cisco ACE, F5, or some other external solution. This requires us to buy a solution and may be the best option. 

2. We could make a VM that runs HA-Proxy on it that redirects to the master nodes.  The problem with this solution is now we need to make sure that VM is redundant and has a VIP, so we haven't solved the problem, just kicked the can down the road. 

3. We can use something like MetalLB and let Kubernetes run the load balancer and thus let it be a part of our solution. 

We will attempt to use the last option.  The problem here is that before we install the master node, we need to have MetalLB.  But before we have MetalLB, we need a working Kubernetes cluster.  So now we have some circular dependencies with no way to break into the egg. 

## Kubeadm

We begin by installing a single master node as the kubernetes master. It is worth pausing here to know that before we do this we should understand which networking overlay we will be using.  

As the ```root``` user on the first master node run: 

```
kubeadm init
```
or
```
sudo kubeadm init
```

When the command finishes a message will display showing how to join this cluster.  Example:

```
You can now join any number of machines by running the following on each node
as root:

  kubeadm join 172.28.225.133:6443 --token aib71v.f4jnd95tb36ig1um --discovery-token-ca-cert-hash sha256:14f0d71c876668669234d6602732d9e3ff2e493ea54576804e59bdbd2a950313
```

### Troubleshooting

If you get an error like: 

```
unable to get URL "https://dl.k8s.io/release/stable-1.11.txt": Get https://dl.k8s.io/release/stable-1.11.txt: dial tcp 23.236.58.218:443: i/o timeout
```
Then your internet connection may be bad or you are behind a firewall.  We can set the proxy to get past this by running the command with the ```https_proxy``` in it: 

```
sudo https_proxy=proxy.esl.cisco.com:80 \ 
no_proxy=localhost,10.96.0.0/12,172.28.225.0/24 \
kubeadm init
```

Here in the ```no_proxy``` we have specified that localhost, the pod CIDR network, and the cluster network are not going through the proxy.  


### Adding the nodes

```
for i in $(seq 4); do ssh kubec0$i sudo https_proxy=proxy.esl.cisco.com:80 no_proxy=localhost,10.96.0.0/12,172.28.225.0/24 kubeadm config images pull; done
```
On each node we need to add the node to the kubernetes cluster using the command specified when we created the master node: 

```
sudo kubeadm join 172.28.225.133:6443 --token aib71v.f4jnd95tb36ig1um --discovery-token-ca-cert-hash sha256:14f0d71c876668669234d6602732d9e3ff2e493ea54576804e59bdbd2a950313
```

Make sure you don't get any errors here (hopefully not!)  If you do: 

* Check the token that it is the right one (not the one in the command up above as that is particular to this test cluster)
* Check your nodes can ping/ssh to your master node. 
* Make sure that the master node did indeed finish with any errors. 

### Accessing your Kubernetes cluster

On the master node, let's see if the setup worked as expected:

```
ssh kubec-master-01
```

Now let's add the environment variables correctly: 

```
mkdir -p $HOME/.kube
ubuntu@kubec-master-01:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
ubuntu@kubec-master-01:~$ sudo chown $(id -u):$(id -u) $HOME/.kube/config
```

Now from the master node determine the state of your cluster: 

```
kubectl get nodes
NAME              STATUS     ROLES     AGE       VERSION
kubec-master-01   NotReady   master    2h        v1.11.3
kubec01           NotReady   <none>    6m        v1.11.3
kubec02           NotReady   <none>    6m        v1.11.3
kubec03           NotReady   <none>    6m        v1.11.3
kubec04           NotReady   <none>    5m        v1.11.3
```

The reason your nodes are not ready is because the cluster networking hasn't been added yet.  



## Install Helm

Download the latest binary release from the [helm repo](https://github.com/helm/helm/releases). 


```
https_proxy=proxy.esl.cisco.com:80 wget https://storage.googleapis.com/kubernetes-helm/helm-v2.11.0-linux-amd64.tar.gz
tar zxf helm-v2*
sudo mv linux-amd64/helm /usr/local/bin/
```

Install Tiller:

```
helm init
```

Proxy configurations:

```
https_proxy=proxy.esl.cisco.com:80 no_proxy=localhost,172.28.225.133 helm init
```
(Where 172.28.225.133 is the kubernetes master node)


# Install Rook

```
https_proxy=proxy.esl.cisco.com:80 no_proxy=localhost,172.28.225.133 helm repo add rook-beta https://charts.rook.io/beta
```
