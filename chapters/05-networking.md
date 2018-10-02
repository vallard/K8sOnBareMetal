# Chapter 5: Kubernetes Networking

### Calico

We will use Calico as a simple way to get started with networking on Kubernetes.  

Download the Calico YAML files: 

```
https_proxy=proxy.esl.cisco.com:80 wget https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/rbac-kdd.yaml
https_proxy=proxy.esl.cisco.com:80 wget https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml
```

If you only did ```kubeadm --init``` when you set up Kubernetes, we need to modify the ```/etc/kubernetes/manifests/kube-controller-manager.yaml``` file to add the ```cidr-network```: 

```diff
- command:
    - kube-controller-manager
    - --address=127.0.0.1
    - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
    - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key
+   - --cluster-cidr=192.168.0.0/16
+   - --allocate-node-cidrs=true
    - --controllers=*,bootstrapsigner,tokencleaner
    - --kubeconfig=/etc/kubernetes/controller-manager.conf
    - --leader-elect=true
    - --root-ca-file=/etc/kubernetes/pki/ca.crt
    - --service-account-private-key-file=/etc/kubernetes/pki/sa.key
    - --use-service-account-credentials=true  
```

Then you can kill the pod that runs the controller and restart it.  

```
kubectl get pods -n kube-system | grep controller
```

Then kill it.  By restarting it will automatically re-read the configuration: 

```
kubectl delete pod -n kube-system kube-controller-manager-kubec-master-01
```

### Troubleshooting

At this point all nodes should come up with:

```
kubectl get nodes -o wide
NAME              STATUS    ROLES     AGE       VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
kubec-master-01   Ready     master    21h       v1.11.3   172.28.225.133   <none>        Ubuntu 18.04.1 LTS   4.15.0-20-generic   docker://17.12.1-ce
kubec01           Ready     <none>    18h       v1.11.3   172.28.225.139   <none>        Ubuntu 18.04.1 LTS   4.15.0-20-generic   docker://17.12.1-ce
kubec02           Ready     <none>    18h       v1.11.3   172.28.225.140   <none>        Ubuntu 18.04.1 LTS   4.15.0-20-generic   docker://17.12.1-ce
kubec03           Ready     <none>    18h       v1.11.3   172.28.225.143   <none>        Ubuntu 18.04.1 LTS   4.15.0-20-generic   docker://17.12.1-ce
kubec04           Ready     <none>    18h       v1.11.3   172.28.225.144   <none>        Ubuntu 18.04.1 LTS   4.15.0-20-generic   docker://17.12.1-ce
```
They should all say ready.  Now make sure all pods are up: 

```
kubectl get pods --all-namespaces
NAMESPACE     NAME                                      READY     STATUS              RESTARTS   AGE
kube-system   calico-node-4jlbm                         2/2       Running             0          13m
kube-system   calico-node-52nct                         2/2       Running             0          13m
kube-system   calico-node-b2fjc                         2/2       Running             0          13m
kube-system   calico-node-cdhpd                         2/2       Running             0          13m
kube-system   calico-node-lkr7w                         2/2       Running             0          13m
kube-system   coredns-78fcdf6894-mm4lt                  0/1       ContainerCreating   0          8m
kube-system   coredns-78fcdf6894-t4kq5                  0/1       ContainerCreating   0          8m
kube-system   etcd-kubec-master-01                      1/1       Running             2          21h
kube-system   kube-apiserver-kubec-master-01            1/1       Running             2          21h
kube-system   kube-controller-manager-kubec-master-01   1/1       Running             2          4m
kube-system   kube-proxy-22x7z                          1/1       Running             0          18h
kube-system   kube-proxy-928gr                          1/1       Running             0          18h
kube-system   kube-proxy-bjwps                          1/1       Running             4          21h
kube-system   kube-proxy-cx64p                          1/1       Running             0          18h
kube-system   kube-proxy-q7vxj                          1/1       Running             0          18h
```

Here we see that the coredns pods seem to be hung.  We can see why by examining the pod: 

```
kubectl describe pod -n kube-system coredns-78fcdf6894-t4kq5
```

The main error we see is:

```
cfe76cb4552a168dcdd5dbd57c972c64550d1b16459d3517259a5ed9081b7b" network for pod "coredns-78fcdf6894-t4kq5": NetworkPlugin cni failed to set up pod "coredns-78fcdf6894-t4kq5_kube-system" network: no podCidr for node kubec02
```

This means that the pod cidr was not allocated to the node.  To change this modify the ```/etc/kubernetes/manifests/kube-controller-manager.yaml``` file as specified above. 

At this point all kubernetes nodes and pods should be working properly.  

```
kubectl get pods -n kube-system
NAME                                      READY     STATUS    RESTARTS   AGE
calico-node-4jlbm                         2/2       Running   0          28m
calico-node-52nct                         2/2       Running   0          28m
calico-node-b2fjc                         2/2       Running   0          28m
calico-node-cdhpd                         2/2       Running   0          28m
calico-node-lkr7w                         2/2       Running   0          28m
coredns-78fcdf6894-mm4lt                  1/1       Running   0          24m
coredns-78fcdf6894-t4kq5                  1/1       Running   0          24m
etcd-kubec-master-01                      1/1       Running   2          21h
kube-apiserver-kubec-master-01            1/1       Running   2          21h
kube-controller-manager-kubec-master-01   1/1       Running   1          6s
kube-proxy-22x7z                          1/1       Running   0          19h
kube-proxy-928gr                          1/1       Running   0          19h
kube-proxy-bjwps                          1/1       Running   4          21h
kube-proxy-cx64p                          1/1       Running   0          19h
kube-proxy-q7vxj                          1/1       Running   0          19h
kube-scheduler-kubec-master-01            1/1       Running   3          21h
```

# Verifying CoreDNS works

To verify CoreDNS works we usually install busybox and verify with the ```nslookup``` command.  Based on [this issue](https://github.com/kubernetes/kubernetes/issues/66924) we will use verison ```1.28.4```. 

```
kubectl run bb --image=busybox:1.28.4 -- sleep 30000
```

Now we can run nslookup on the CoreDNS service to make sure it works: 

```
kubectl exec -it bb-7d67b4bc88-b4clt nslookup kubernetes
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      kubernetes
Address 1: 10.96.0.1 kubernetes.default.svc.cluster.local
```

This is great to make sure all our services are working.  

### Installing MetalLB

We want a load balancer for all our services as well as for the redundant master capabilities.  

```
https_proxy=proxy.esl.cisco.com:80 wget https://raw.githubusercontent.com/google/metallb/v0.7.3/manifests/metallb.yaml
kubectl apply -f metallb.yaml
```

We can then create a configuration map ```metallb-layer2-config.yaml``` that includes the IPs we can dole out to the different services: 

```
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: my-ip-space
      protocol: layer2
      addresses:
      - 172.28.225.186-172.28.225.188
      - 172.28.225.184/32
      - 172.28.225.160/32
      - 172.28.225.134/32
```
 
Applying this configuration and now we have a load balancer: 

```
kubectl apply -f metallb-layer2-config.yaml
```

We can test this load balancer by launching a quick test nginx application: 

```
kubectl run ngx01 --image=nginx
```
Then expose the service: 

```
kubectl expose deployment ngx1 --port 80
```

You will then see it was assigned an IP address: 

```
kubectl get svc
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)        AGE
kubernetes   ClusterIP      10.96.0.1      <none>           443/TCP        23h
ngx1         LoadBalancer   10.111.46.81   172.28.225.186   80:31956/TCP   31s
```

You should now be able to open a web browser to the external IP address.  (In my case it used ```172.28.225.186```).  Your app is up and Kubernetes is cranking!

 

