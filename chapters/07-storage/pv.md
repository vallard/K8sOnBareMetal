# 7.3 Persistent Volumes

Persistent volumes are first class Kubernetes resources just as pods are.  The kinds of persistent volumes available to the users are generally performed by an administrator and depend on which Kubernetes platform we are running on.  Since we are running this in our own data center we would not have access to a google block storage device, but we have many more options we can add.  

The way it works is that an administrator defines different `persistentVolume`s amd makes them available to the cluster.  Next they can abstract them making `storageClass`es.  The name of the `storageClass` is arbitrary and can be the same name in public or private clouds.  When a user wants to use a particular `storageClass` they create a `persistentVolumeClaim`.  This `persistentVolumeClaim` is then mounted as a `Volume` to the pod.  In the previous chapter we talked about different volumes that could be mounted.  A `persistentVolumeClaim` is just another type of volume that can be mounted but abstracts the storage underneith it making it transparent to the user.  

Let's explore the case of using NFS as a persistent volume. 

# 7.2.1 NFS Persistent Volume

The NFS driver for Persistent Volumes is similar to the one we saw for drivers.  Here we create a persistent volume with a yaml file again called `nfs-pv.yaml`:


```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfsvol01
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: general
  mountOptions:
    - hard
    - intr
  nfs:
    server: 172.28.225.138
    path: /nfs/vol1/pg1

```
A few options are worth noting: 

1. The `kind` is `PersistentVolume` showing it is a native Kubernetes type. 
2. We are able to specify the `capacity`.  This is the total amount of space we could use from this volume. Notice that we are using `5Gi` which is 5 Gibabytes.  
3. The `volumeMode` shows it is a filesystem.  If an iSCSI or other block device were mounted you could instead set this to `raw`.  `filesystem` is the default.
4. `AccessMode` here is `ReadWriteMany` which means that many pods can read and write in this directory at the same time.  Other options that can be used include `ReadWriteOnce` which only allows one Pod read/write access or `ReadOnlyMany` which allows many to just read. 
5. `persistentVolumeReclaimPolicy` is set here to `recycle`.  This means that it will just delete the contents of the filesystem on the NFS server when the persistent volume is destroyed.  However, it will persist if a Pod detaches from the PV.  Other options include: 
	*	`Retain` which keep the contents of the volume after a Persistent Volume is destroyed.
	* `Delete` which will delete the volume.  This is used in cloud or cinder/CEPH volumes as we'll see soon enough. 
6. NFS also includes a few mount options that get passed along to the options of how NFS is mounted.  `hard` and `intr` says that NFS will continually retry to contact the NFS server and the program using NFS will continue executing after where the server crashed. The default `soft` option will make the program crash immediately if the NFS server is not reachable.  The `intr` allows the NFS requests to be interrupted (making it close to a soft mount) if the user wants to terminate the program in the event of an NFS server failure. 

Creating this volume is done with

```
kubectl create -f nfs-pv.yaml
```
We can see the output after it is created:

```
kubectl get pv
NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM     STORAGECLASS   REASON    AGE
nfsvol01   5Gi        RWX            Recycle          Available             general                  4s
```
Note that even if you didn't have NFS set up correctly a persistent volume could still be created.  

# 7.2.2 NFS StorageClass

Now that we have our persistent volume we will want to abstract it so the user doesn't need to know that it is NFS.  In the previous definition of the `nfsvol01` above we gave it a `storageClass` of `general`.  This name could be whatever we want.   