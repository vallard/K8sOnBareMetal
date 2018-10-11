# Introduction

This is a guide for installing Kubernetes on Bare Metal servers in a data center.  Most guides assume you are running on a VM whether in a private data center or in a public cloud.  As such they omit many details that can help an organization be successful deploying on-prem.  In this section we will lay the groundwork for why this is something important for organizations to consider.  

## Kubernetes: The great leveller

One of the great benefits of Kubernetes is it levels the playing field for Platform as a Serivice (PaaS) providers as well as Infrastructure as a Service (IaaS) providers.  In the case of IaaS we now have a consistent way (```kubectl```) of launching applications on infrastructure that works the same in public clouds or in your own data center.  The differences of how networking or persistent storage is abstracted away by Kubernetes.  

PaaS providers on the other hand have gone through significant disruption due to popularization of containers and Kubernetes.  It used to be a PaaS provider would give an opinionated framework with custom interfaces to run applications.  Now, most of them have shifted to giving an opinion on how to run Kubernetes.  In fact, all major PaaS and IaaS providers offer Kubernetes solutions.  

But if Kubernetes levels the field with IaaS and PaaS then it does it more so to bridge the gulf between Public Clouds and Private Clouds.  The promise of OpenStack which once offered the closest thing to AWS EC2 in the data center was never realized.  Many reasons exist, but one reason [OpenStack became boring](https://www.mirantis.com/blog/careful-wish-openstack-finally-boring/) was because it fell too far behind what public clouds were able to do.  With Kubernetes we can realize the same solution in our own data center that we can in AWS, Azure, or GCP.  The same Kubernetes version that runs on the big three cloud providers can run in your own data center.  

## Warnings about this Guide

### Automation

As you start skimming chapters you'll say to yourself:  "Hey, we should automate this stuff, why aren't we using Ansible or something else to make it better?".  The answer is: Yes, you absolutely should.  But this guide is written in such a way that you understand the tasks required and can automate them yourself.  I've automated many of these tasks since 2016 with Ansible and Terraform but this time wanted to just get the principles down.  Consider it similar to [Kelsey Hightower's the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) but for bare metal.

### Applications to Public and Private and Virtual Machines

Even if you are running your Kubernetes on Virtual Machines in the cloud this guide will still be useful.  Cloud providers allow you to skip details of providing storage, load balancers, network constructs, or installing Kubernetes all together.  In this guide you'll see how to implement Kubernetes all the way down. Though we don't profess that public clouds use the methods presented here, you will hopefully gain an understanding of how it could be implemented in the cloud.  

Armed with this knowledge you will be in a better position to build a true hybrid cloud solution where your users will not know the difference between running on your own data center Kubernetes cluster or one that lives in the public cloud. 

## Why You Shouldn't Read this Guide

Installing Kubernetes and running it yourself results in doing tasks that AWS likes to call: ["Undifferentiated Heavy Lifting"](https://www.cio.co.nz/article/466635/amazon_cto_stop_spending_money_undifferentiated_heavy_lifting_/).  Meaning, you do all this work and its not going to help you sell any more widgets.  In many cases you can get it faster and cheaper by just standing Kubernetes up using the many public cloud providers.  They are secure, and the professionals that run them probably know how to run Kubernetes better than you do.  

But in spite of public cloud providers best attempts to sell you their services by telling you that it is pointless to role your own you know deep down inside as an engineer that there is no "best way" but that instead everything is about trade offs.  We pick between convenience or data privacy, cost or time, good weather or sanity by not living near millions of angry silicon valley drivers.  The choice is yours and we optimize for what makes sense for our lives and the companies we work for.  Yes, that was a deep thought.  

## OnPrem vs. Public Cloud Providers

Let us examine several tradeoffs between running Kubernetes on-prem vs in a public cloud.

### Performance

In 2017, Stratoscale published an article [1](https://www.stratoscale.com/blog/containers/running-containers-on-bare-metal/) about the performance between bare metal and VMs. The VMs in question were run on EC2.  While I can not substantiate the claims, the article shows there is a 7x-9x performance improvement in running containers on bare metal.

To counter this a colleague at Google mentioned:  "The unique thing about cloud is that you can throw 5000 nodes at a cluster, create 50 clusters per zone, pay per second of use and save 80% extra using preemptible nodes.  If you want performance, scale out!

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Interesting to add to that mix cost per work unit and ability to scale.<br><br>The unique thing about cloud is that you can throw 5000 nodes at a cluster, create 50 clusters per zone, pay per second of use and save 80% extra using preemptible nodes.<br><br>If you want performance, scale out!</p>&mdash; Pablo Carlier (@pablocarlier) <a href="https://twitter.com/pablocarlier/status/1050078195054272512?ref_src=twsrc%5Etfw">October 10, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

The trade off here is whether you consistently have a steady workflow or have massive scaling needs during peak seasons.  By having a public and private Kubernetes instance, you can have both and keep costs low. 

### Costs

There are tradeoffs of where to deploy capital both human or money.  It is rarely cheaper in terms of dollars to rent a server from a cloud provider than to simply buy your own server. [2](https://blog.serverdensity.com/cloud-vs-colocation/) 

However, it is often more expensive to manage that environment than to pay the cloud provider to that for you.  

Building a Kubernetes cluster on prem does not keep you from enjoying the pace of innovation from public cloud providers.  In fact, if anything Kubernetes allows true hybrid cloud computing.  [The Service Catalog](https://kubernetes.io/docs/concepts/extend-kubernetes/service-catalog/) from Kubernetes uses the Open Service Broker API to present cloud services such as message queues, data search tools, and others to Kubernetes clusters.  

Finally, consider the cost of renting GPUs in a public cloud.  While it is great that they can be scaled, if it is something you might use a lot, (Such as Jupyter notebooks backed by Tensorflow on GPUs) than it can save significant cost running on prem. 

The tradeoff here is if your bill is astronomical in the public cloud, you may consider repatriating some workloads to save cost. You can still have the innovation of public clouds.  Kubernetes is the great leveller.


### Data Sovereignty

Data sovereignty is the concept that information which has been converted and stored in binary digital form is subject to the laws of the country in which it is located [1](https://whatis.techtarget.com/definition/data-sovereignty).  Many organizations have no choice but must run their applications on-prem.  Even though there are many government approved public cloud offerings, there are still reasons for people to protect and want to own their data. Running Kubernetes on Prem can give you many of the same benefits you would get from your data in a public cloud in the sweet home comfort of your own datacenter.  

### Control and Customization

At present there are some features you may like that are not provided by public cloud providers Kubernetes offereings[4](https://kubedex.com/google-gke-vs-microsoft-aks-vs-amazon-eks/).  This might include redundant masters, locations, or custom networking.  

Care should be taken to decide whether these customizations are really necessary and that if you were to use them it could lead to delays on project deliveries, but hey, that's one reason this guide exists!

## Virtual Machines vs. Bare Metal

It is much easier to manage virtual machines than bare metal machines.  Virtual machines can be created and destroyed in a fraction of the time that it takes to get a physical machine installed and ready.  Remote management of virtual machines is also easier.  

The other benefit of Virtual Machines is that they are able to more efficiently use the resources of a physical machine.  It was common 5 years ago for VMware users to report how efficiently utilized their resources were.  

On the other hand, running containers on virtual machines can feel like you are roller skating on top of a skateboard.  VMware is not cheap and many of the features it offers are not necessary to container workloads.  We don't care if a pod goes down because Kubernetes will restart it.  If a machine goes down, Kubernetes will redistribute the workers.  We don't need VMware HA to do that for us.  

In addition deploying a virtualization solution adds another layer of complexity.  One must update the VMware components, manage more virtual switches (portgroups for vMotion, storage, etc), and in many cases manage an external storage.  One of the promises bare metal Kubernetes gives us that we'll explore in this guide is that Kubernetes can manage our storage for us giving us a total Kubernetes hyperconverged solution.  

The tradeoff here are skills and workloads:  VMware skills vs. Linux skills.  But they can always be used in conjunction.  It is possible to build a Kubernetes system with bare metal worker nodes (to get performance) and run the Kubernetes master nodes as VMs. But note, in large scale deployments, etcd will be very resource intensive and may warrent running on bare metal. 

## Roll Your Own (RYO) vs. Buying 

As mentioned before, most PaaS providers have morphed into Opinionated Kubernetes providers. 

One great thing vendors provide is support.  If you run into Kubernetes issues then your vendor is on the hook to get you set up right. If you think running your own is a science experiment then maybe going with Enterprise backed support is a good thing.  

Many Kubernetes vendors, however, claim that they follow as close to upstream as possible.  If something is wrong with the upstream, then an issue can be filed pretty quickly and the turn around on Kubernetes, especially for core features is better than many vendor support cycles that have been out there in the wild. 


## Architecture of a Bare Metal Kubernetes Cluster