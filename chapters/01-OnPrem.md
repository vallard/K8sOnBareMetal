# Introduction

This is a guide for installing Kubernetes on Bare Metal servers in a data center.  In many cases you may be behind a corporate firewall and require proxies to access internet resources.  That has been considered in here as well. 

You may also think to yourself:  "Hey, we should automate this stuff, why aren't we using Ansible or something else to make it better?".  The answer is: Yes, you probably should do that but this guide is written in such a way that you understand the tasks required and can automate them yourself.  I've automated these tasks back in 2016 with Ansible and Terraform but this time wanted to just get the knowledge down.  Consider it similar to [Kelsey Hightower's the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) but for bare metal.

## Why You Shouldn't Read this Guide

Installing Kubernetes and running it yourself results in doing tasks that AWS likes to call: ["Undifferentiated Heavy Lifting"](https://www.cio.co.nz/article/466635/amazon_cto_stop_spending_money_undifferentiated_heavy_lifting_/).  Meaning, you do all this work and its not going to help you sell any more widgets.  In many cases you can get it faster and cheaper by just standing Kubernetes up using the many public cloud providers.  They are secure, and professionals and probably know how to run Kubernetes better than you do.  

But in spite of public cloud providers best attempts to sell you their services by telling you that it is pointless to role your own you know deep down inside as an engineer that there is no "best way" but that instead everything is about trade offs.  We pick between convenience or data privacy, cost or time, good weather or sanity by not living near millions of angry silicon valley drivers.  The choice is yours and we optimize for what makes sense for our lives and the companies we work for.  Yes, that was a deep thought.  

## OnPrem vs. Public Cloud Providers



## Virtual Machines vs. Bare Metal

## Roll Your Own (RYO) vs. Buying 
