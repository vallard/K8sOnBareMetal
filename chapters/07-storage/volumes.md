# 7.2 Volumes

We already explained a use case of how kubeless uses volumes.  Let's go through an example of a volume to make things more concrete.  In this example we'll use an NFS volume. 

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




