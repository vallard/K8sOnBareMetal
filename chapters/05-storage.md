# Application Storage

# Kubernetes Storage

## 5.1 Introduction and Overview

### 5.1.1 Containers are Ephemeral 
Microservices are all about stateless systems.  Even kubernetes itself services such as the API service, the controller and scheduler all run stateless, getting their data from [etcd](https://coreos.com/etcd/)

We can launch deployments and then go change the runing containers but when they restart, all changes are lost. 

This was the original design of kubernetes and microservices:  Applications should be stateless and state should be a service that lives elsewhere.  We've come a long way since then and Kubernetes has evolved to give us persistence.  

Let's first look at the default behavior.  Consider the case of our favorite Nginx web service.  We can start a container and expose the service: 

```
kubectl run nx --image=nginx 
kubectl expose deployment nx --port=80 --target-port=80 --type=LoadBalancer
```

Now we can visit this service in our web browser and see the normal nginx welcome screen. 

![img](images/storage01.png)


Now let's edit the pod: 

```
kubectl get pods -l run=nx
...
nx-d8f5c6d58-dt7gj ....
...
```
We can now log into it: 

```
kubectl exec -it nx-d8f5c6d58-dt7gj /bin/bash
# now on the pod
root@nx-d8f5c6d58-dt7gj:/# cd /usr/share/nginx/html/
root@nx-d8f5c6d58-dt7gj:/usr/share/nginx/html# echo "hello from this pod" > index.html
```

Refreshing the page we get: 

```
hello from this pod
```

But by deleting the pod: 
 
```
root@nx-d8f5c6d58-dt7gj:/usr/share/nginx/html# exit
kubectl delete pod nx-d8f5c6d58-dt7gj
```

And refreshing the page, we get the nginx welcome site again.  

## 5.2 Volumes

Kubernetes has the concept of Volumes.  Volumes are a way to have storage be independent of the Pod but provisioned as part of a workload like any other Kubernetes resource.  

Volumes are defined as part of the pod definition:

```
   spec:
      containers:
      - image: nginx
        name: ngxnfs
        volumeMounts:
          - name: nfsvol
            mountPath: /usr/share/nginx/html/
```
In the above we see there is some volume named `nfsvol` and it is mounted on the container at the `/user/share/nginx/html` path.  Whatever creates the nfsvol is independent of the container.  `nfsvol` can be AWS Elastic Block Storage, a file on a local node, resource in Kubernetes or anything.  And that volume part must also be defined as part of the definition. 

Other properties of Volumes include: 

* __Plugins__ Both volumes have the idea of 'plugins' where different backends can be added.  This includes the usual public cloud suspects, Ceph, NFS, local disks, and up and coming kubernetes storage providers. Different plugins have different implementations.  Some will persist when the containers are gone, others will be destroyed. 

* __Containers Share the Storage__ As noted, a Pod can consist of multiple containers.  Often there is only one container per pod, but in cases where multiple containers are in the same pod and need to share some type of data, these containers will share the storage volume.  

* __Predefined By Administrator__ Depending on your kubernetes environment different volume plugins will be available to users. Naturally, on a Kubernetes cluster running internally you wouldn't expect to be able to consume an AWS EBS volume. What can be used is dependent on where the pods are running.  We will talk about ways to abstract this later.

* __Many types can be used at the same time__ If you have a container that requires iSCSI, NFS, Ceph, and an empty filesystem then these can all be defined on the same system and used by the same pod.  While this is pretty ridiculous, its nice to know that Kubernetes is quite capable. 

### 5.2.1 Kubeless Use case

Let's examine a use case. [`kubeless`](https://kubeless.io) is a function as a service implementation for Kubernetes.  As part of kubeless a user will submit code that might be written in golang which can then be called from an API.  How does kubeless do this?  It uses the concept of an `initContainer`.  An `initContainer` is a container that runs a job before the main container in the pod will start running.  The `initContainer` takes the code submitted by the user and compiles it along with the preexisting code the container has.  It uses the `emptydir` plugin which takes a local directory on the node the pod is placed on and compiles into that directory.  Next the runtime container takes the compiled code and executes it as its main command.  The volume is only required for the lifetime of the pod. 

## 5.3 NFS Volume Example

Let's illustrate a way we could provision a volume for consumption in our data center using NFS. 

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
          path: /nfs/vol1/nginx/html
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

## 5.4 ConfigMaps & Secrets

There are two volumes that are used quite a lot in Kubernetes that represent configuration for applications or secrets that might be needed by the application.  Let's take a look at these with an example. 

### 5.4.1 Kubernetes Secrets

The twelve factor app was introduced to the world around 2011 by developers at PaaS providers Heroku.  In this "manifesto" 12 important attributes of SaaS based applications are defined.  This manifesto is somewhat of an ancestor to today's microservices.  

One of the important take-aways from the 12 factor app manifesto is that applications should never store config data or important data like passwords, keys, or other sensative information.  The arguments are that this is insecure and not best practices.  The solution is to store this information in environment varables.  

In a kubernetes environments, how can we get things like database passwords to an environment variable?  We could pass the environment variable as part of the pod.yaml file but the pod.yaml file is usually checked in with the code.  The answer is that we use [secrets](https://kubernetes.io/docs/concepts/configuration/secret/). 

Secrets are a yaml file that inject environment variables or files into a pod if we use them as volumes.  

### 5.4.2 ConfigMap

A [ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/) holds configuration information for a pod.  By decoupling the configuration information from a Pod we can run a pod in different kubernetes environments. It's similar to Kubernetes secrets but the contents are usually less sensitive and they are not base64 encoded. 

### 5.4.3 Volex Example with ConfigMap and Secrets

Let's first deploy a standard flask python application that can read environment variables. This example will look like a standard web page:

```
kubectl create -f https://raw.githubusercontent.com/vallard/K8sOnBareMetal/master/chapters/05-storage/volex/volex.yaml
```

From this you will see a (not-so) nice page of generic HTML that doesn't look too interesting. 

![img](images/storage02.png) 

The [python code](https://github.com/vallard/K8sOnBareMetal/blob/master/chapters/05-storage/volex/showall.py) however shows things could be different depending on whether some files are defined.  

The code looks like: 

```python
#!/usr/bin/env python
from flask import Flask, render_template
import os
app = Flask(__name__)
@app.route('/')
def hello_world():
    username = "not defined"
    password = "not defined"
    bgcolor = "#aaa"
    textcolor = "#000"
    user_file = "/tmp/projected/secrets/username"
    password_file = "/tmp/projected/secrets/password"
    bgcolor_file = "/tmp/projected/configmap/bgcolor"
    textcolor_file = "/tmp/projected/configmap/textcolor"
     
    if os.path.exists(user_file):
        with open(user_file) as f:
            username = f.readlines() 
    if os.path.exists(password_file):
        with open(password_file) as f:
            password = f.readlines() 
    if os.path.exists(bgcolor_file):
        with open(bgcolor_file) as f:
            bgcolor = f.readlines() 
    if os.path.exists(textcolor_file):
        with open(textcolor_file) as f:
            textcolor = f.readlines() 

    return render_template('showall.html', 
            username = username, 
            password = password, 
            textcolor = textcolor,
            bgcolor = bgcolor)

if __name__ == '__main__':
app.run(debug = True)
```

Notice that in the above code we are looking for four different files that define the username, password, bgcolor, and text color.  We can define these by adding a configmap and some secrets.

#### 5.4.3.1 Adding the ConfigMap  

Let's create a configmap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: volex
  labels:
    name: volex
  namespace: default
data:
  bgcolor: "#000"
  textcolor: "#fff"
  config: |-
    ---
    :version: 1.0
    :logfile: /var/log/volex.log

```

We've added `bgcolor`, `textcolor`, and `config`.  Config is a file that could contain lots of configuration information, like logging or other configuration parameters a server might want.  For us, we're just interested in `bgcolor` and `textcolor`.  

Now that we have these, we need to mount them as a volume.  We can edit our pod definition by adding: 

```yaml
...
       volumeMounts:
          - mountPath: /tmp/projected
            name: volex-vol
      volumes:
      - name: volex-vol
        configMap:
          name: volex
          items:
          - key: bgcolor
            path: configmap/bgcolor
          - key: textcolor
            path: configmap/textcolor
...
```

To our pod definition.  Here in the `spec` we add `volumeMounts`.  This references the volume named `volex-vol` defined below.  We give it a mount path as to where the configMap should be mounted.  Here we are telling it to go to `/tmp/projected`.  

Below in the `volumes` section we tell it that `volex-vol` is of type `configMap` so Kubernetes knows to use the `configMap` plugin (which is actually built into Kubernetes).  By specifying the key `bgcolor` and the file `configmap/bgcolor` then adding this to the `mountPath` above, we find that the pod will have a file in `/tmp/projected/configmap/bgcolor`.  This is exactly what the python flask server expects above.  It can now read in the parameters.  

Let's create these resources with: 

```
kubectl create -f https://raw.githubusercontent.com/vallard/K8sOnBareMetal/master/chapters/05-storage/volex/configmap.yaml
```
Either manually update with `kubectl edit deployment volex` or apply with: 

```
kubectl apply -f https://raw.githubusercontent.com/vallard/K8sOnBareMetal/master/chapters/05-storage/volex/volex-cfm.yaml
```



Since we've set our background color to black (#000) and the text white (#fff) refreshing after applying this configuration gives us: 

![img](images/storage03.png)

Notice, that if you define the pod and don't actually have a volume with configmap named `volex` the pod will never load.  That's actually true of any volume.  If the pod is referencing a volume that doesn't exist, the pod will never run. 

#### 5.4.3.2 Adding Secrets  

Let's now add some secrets. Let's suppose this app connected to a database.  We would then need a username and password.  Let's suppose our username is `beyonce` and the password is `putaring0n!t`.  To create secrets, we first need to base64 encode these items:

```
echo -n beyonce | base64
YmV5b25jZQ==
echo -n 'putaring0n!t' | base64
cHV0YXJpbmcwbiF0
```
(note: we had to put 's around the password because it contained a `!`. )
These values we add to our secrets file: 

```
apiVersion: v1
kind: Secret
metadata:
  name: volex
type: Opaque
data:
  username: YmV5b25jZQ==
  password: cHV0YXJpbmcwbiF0
```

We then create this secret:

```
kubectl create -f secret.yaml
```

Alternatively you can create from an already created secret on the internet: 

```
kubectl create -f https://raw.githubusercontent.com/vallard/K8sOnBareMetal/master/chapters/05-storage/volex/secret.yaml
```

Now how can we mount this volume?  The script expects all items to be mounted in the same directory.  But if we try that we get an error as each volume can only be mounted at one spot.  We did use subdirectories so we can use that for the secrets:

```
...
      volumeMounts:
        - mountPath: /tmp/projected
          name: volex-vol
        - mountPath: /tmp/projected/secrets
          name: volex-secret
...
     volumes:
      - configMap:
          items:
          - key: bgcolor
            path: configmap/bgcolor
          - key: textcolor
            path: configmap/textcolor
          name: volex
        name: volex-vol
      - name: volex-secret
        secret:
          items:
          - key: username
            path: username
          - key: password
            path: password
          secretName: volex
...
```

Modify your `volex` deployment with: 

```
kubectl apply -f https://raw.githubusercontent.com/vallard/K8sOnBareMetal/master/chapters/05-storage/volex/volex-cm-secrets.yaml
```

Running this we now get our secrets.  By refreshing our webpage we can see the secrets and the configMap information in the Pod: 

![img](./images/04.png)














