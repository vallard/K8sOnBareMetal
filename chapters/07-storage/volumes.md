# 7.2 Volumes

We already explained a use case of how kubeless uses volumes.  Let's go through an example of a volume to make things more concrete.  In this example we'll use an NFS volume. 

## 7.2.1 NFS Volume Example

Our NFS server is a simple ubuntu server running NFS.  We followed [simple instructions](https://www.smarthomebeginner.com/install-configure-nfs-server-ubuntu/) to create a volume called `/nfs/vol1` on the server with IP address `172.28.225.138`.  

An important note that for NFS to work the worker nodes that are using NFS will need to have an nfs client installed at the host level.  For our ubuntu servers we run: 

```
sudo apt-get install nfs-client
```

In this directory on the NFS server we can prepopulate an `index.html` that can be mounted to our pods that they can serve.   

We create an nginx deployment that looks as follows: 

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    run: ngxnfs
  name: ngxnfs
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      run: ngxnfs
  template:
    metadata:
      labels:
        run: ngxnfs
    spec:
      containers:
      - image: nginx
        name: ngxnfs
        volumeMounts: 
          - name: nfsvol
            mountPath: /usr/share/nginx/html/
      volumes:
      - name: nfsvol
        nfs:
          server: 172.28.225.138
          path: /nfs/vol1
---
apiVersion: v1
kind: Service
metadata:
  labels:
    run: ngxnfs
  name: ngxnfs
  namespace: default
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    run: ngxnfs
  sessionAffinity: None
  type: LoadBalancer
```

When we navigate to the service we see that it has the contents of our NFS server.  We can scale the nodes up and each time we can hit the same IP: 

```
kubectl scale --replicas=5 deployment ngxnfs
```

## 7.2.2 Projected Volume Example

There is often data we want applications running in our pods to get.  A `projected` volume is a way we can combine data from different kubernetes contructs into a single volume.  These kubernetes resources include: 
* `secret`
* `downwardAPI`
* `configMap`
* `serviceAccountTokens`.  

Let's introduce a few of these for our sample we will make.  

### 7.2.2.1 Kubernetes Secrets

The twelve factor app was introduced to the world around 2011 by developers at PaaS providers Heroku.  In this "manifesto" 12 important attributes of SaaS based applications are defined.  This manifesto is somewhat of an ancestor to today's microservices.  

One of the important take-aways from the 12 factor app manifesto is that applications should never store config data or important data like passwords, keys, or other sensative information.  The arguments are that this is insecure and not best practices.  The solution is to store this information in environment varables.  

In a kubernetes environments, how can we get things like database passwords to an environment variable?  We could pass the environment variable as part of the pod.yaml file but the pod.yaml file is usually checked in with the code.  The answer is that we use [secrets](https://kubernetes.io/docs/concepts/configuration/secret/). 

Secrets are a yaml file that inject environment variables or files into a pod if we use them as volumes.  

### 7.2.2.2 ConfigMap

A [ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/) holds configuration information for a pod.  By decoupling the configuration information from a Pod we can run a pod in different kubernetes environments. It's similar to Kubernetes secrets but the contents are usually less sensitive and they are not base64 encoded.  

### 7.2.2.3 Implementing a Projected Volume

In Kubernetes 1.11 projected volumes are an alpha construct.  





