# 7.2 Volumes

We already explained a use case of how kubeless uses volumes.  Let's go through a few examples of volumes to make things more concrete.  We'll first use a generic NFS mount and then move to ConfigMaps and Secrets.  

## 7.2.1 NFS Volume Example


## 7.2.2 Projected Volume Example

There is often data we want applications running in our pods to get.  A `projected` volume is a way we can combine data from different kubernetes contructs into a single volume.  These kubernetes resources include: 

* `secret`
* `downwardAPI`
* `configMap`
* `serviceAccountTokens` 

Let's introduce a few of these for our sample we will make.  

### 7.2.2.1 Kubernetes Secrets

The twelve factor app was introduced to the world around 2011 by developers at PaaS providers Heroku.  In this "manifesto" 12 important attributes of SaaS based applications are defined.  This manifesto is somewhat of an ancestor to today's microservices.  

One of the important take-aways from the 12 factor app manifesto is that applications should never store config data or important data like passwords, keys, or other sensative information.  The arguments are that this is insecure and not best practices.  The solution is to store this information in environment varables.  

In a kubernetes environments, how can we get things like database passwords to an environment variable?  We could pass the environment variable as part of the pod.yaml file but the pod.yaml file is usually checked in with the code.  The answer is that we use [secrets](https://kubernetes.io/docs/concepts/configuration/secret/). 

Secrets are a yaml file that inject environment variables or files into a pod if we use them as volumes.  



### 7.2.2.2 ConfigMap

A [ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/) holds configuration information for a pod.  By decoupling the configuration information from a Pod we can run a pod in different kubernetes environments. It's similar to Kubernetes secrets but the contents are usually less sensitive and they are not base64 encoded.  

### 7.2.2.3 Implementing a Projected Volume

In Kubernetes 1.11 projected volumes are an alpha construct.  Therefore, anything pre Kubernetes 1.11 will require that the feature be enabled.  


### 7.2.2.4 Generic example




