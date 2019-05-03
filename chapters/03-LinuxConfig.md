# Linux Configuration

In many environments many of these components may already be setup for you.  Here we focus on how to do it so you know what happens behind the magic. Once you know you can create your own magic. 

In general we would create an Ansible file to do this for us.  That way all files are set correctly for us. But let's go through manually for understanding.

### ```sudo``` without Password

The first thing we need to do is make sure that when we ssh into the machine we aren't prompted for a password every time we do a ```sudo``` command.  

There is a file called /etc/sudoers that is edited using `visudo`.  However, for the non-vim people (which are becoming more and more each day) it defaults to the nano editor.  Let's restore the glory of `vim` by running: 

```


If we want to be dangerous we could run the following command on every machine: 

```
sudo sed -i 's/^%sudo.*/\%sudo  ALL=(ALL:ALL) NOPASSWD: ALL/' /etc/sudoers
```

That would fix it, but I get a little nervous doing that because once you do it, you lose access to the machine if you make a type-o. If you did that you woudl then need to start all over installing the machine.  You may instead choose to do this part manually by going into each machine and running ```sudo visudo```.  From there you would just make sure you change: 

```
%sudo  ALL=(ALL:ALL) ALL
```

To be:

```
%sudo  ALL=(ALL:ALL) NOPASSWD: ALL
```

Here is how you could do it for all the machines.  Make sure you don't have type-Os!

```
for i in $(seq 3); do ssh -t kubec-master-0$i "sudo sed -i 's/^%sudo.*/\%sudo  ALL=(ALL:ALL) NOPASSWD: ALL/' /etc/sudoers"; done
[sudo] password for ubuntu:
Connection to kubec-master-01 closed.
[sudo] password for ubuntu:
Connection to kubec-master-02 closed.
[sudo] password for ubuntu:
Connection to kubec-master-03 closed.

for i in $(seq 4); do ssh -t kubec0$i "sudo sed -i 's/^%sudo.*/\%sudo  ALL=(ALL:ALL) NOPASSWD: ALL/' /etc/sudoers"; done
...
```

The ```-t``` is specified so that you'll need to type in the password when you do ```sudo```, but thankfully, that's the last time we need to do that!  


#### ```/etc/hosts```

We first add all our servers to /etc/hosts so we don't have to mess with IP addresses.  

```
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
172.28.225.130 kubec-master-01
172.28.225.131 kubec-master-02
172.28.225.132 kubec-master-03
172.28.225.139 kubec01
172.28.225.140 kubec02
172.28.225.143 kubec03
172.28.225.144 kubec04
172.28.225.60 kubec05
172.28.225.61 kubec06
```

#### SSH Setup

We'd like to be able to SSH into the master and worker nodes without having to type passwords.  Let's take care of that now.  

We assume that the server you are on is a Linux/Mac machine and has a public key.  This public key we will copy to the ```~/.ssh``` directory on each node in the ```authorized_keys``` file as this will grant our server access without typing passwords.  


```
for i in $(seq 3); do ssh ubuntu@kubec-master-0$i mkdir -p /home/ubuntu/.ssh; done
for i in $(seq 4); do ssh ubuntu@kubec0$i mkdir -p /home/ubuntu/.ssh; done
```

Copy the keys from your administrator server to the nodes: 
```
for i in $(seq 3); do scp ~/.ssh/id_rsa.pub ubuntu@kubec-master-0$i:/home/ubuntu/.ssh/authorized_keys; done
for i in $(seq 4); do scp ~/.ssh/id_rsa.pub ubuntu@kubec0$i:/home/ubuntu/.ssh/authorized_keys; done
ubuntu@kubec01's password:
id_rsa.pub                                    100%  392     0.4KB/s   00:00
ubuntu@kubec02's password:
id_rsa.pub                                    100%  392     0.4KB/s   00:00
ubuntu@kubec03's password:
id_rsa.pub                                    100%  392     0.4KB/s   00:00
ubuntu@kubec04's password:
id_rsa.pub                                    100%  392     0.4KB/s   00:00
```

Now we dont' need to enter any passwords!  Test it out: 

```
for i in $(seq 3); do ssh ubunbu@kubec-master-0$i date; done
Fri Sep 21 02:28:28 PDT 2018
Fri Sep 21 02:28:27 PDT 2018
Fri Sep 21 02:28:16 PDT 2018
```
```
for i in $(seq 4); do ssh ubuntu@kubec0$i date; done
Thu Sep 20 09:10:43 PDT 2018
Thu Sep 20 09:07:47 PDT 2018
Thu Sep 20 08:07:43 PDT 2018
Thu Sep 20 08:10:26 PDT 2018
```

Here we notice two things:  

1. We can ssh into all machines.  That's good!
2. The clocks are skewed!  That's bad!  We'll get to that later. 

The last thing to note is we don't really like typing in the ```ubuntu``` user name all the time.  We can take care of this by creating/modifying the ```~/.ssh/config``` file.  

```
Compression yes
Host kubec01
        Hostname kubec01
        User ubuntu
Host kubec02
        Hostname kubec02
        User ubuntu
Host kubec03
        Hostname kubec03
        User ubuntu
Host kubec04
        Hostname kubec04
        User ubuntu
Host kubec-master-01
        Hostname kubec-master-01
        User ubuntu
Host kubec-master-02
        Hostname kubec-master-02
        User ubuntu
Host kubec-master-03
        Hostname kubec-master-03
        User ubuntu
```

Now you don't have to specify the ```ubuntu``` user every time you ssh into the node. 



#### Set the Hostname on all nodes

Now let's set the hostname on all the nodes

```
for i in $(seq 3); do ssh kubec-master-0$i sudo hostnamectl set-hostname kubec-master-0$i; done
for i in $(seq 4); do ssh kubec0$i sudo hostnamectl set-hostname kubec0$i; done
```

Verify

```
for i in $(seq 3); do ssh kubec-master-0$i hostname; done
kubec-master-01
kubec-master-02
kubec-master-03
```

```
for i in $(seq 4); do ssh kubec0$i hostname; done
kubec01
kubec02
kubec03
kubec04
```

Easy ssh bliss is now ours!

### Setting the Clocks

Let's get back to the clocks.  One way to get off to a bad start with Kubernetes is to have bad clock setup.  All kinds of issues happen with bad clocks: 
* Can't get new repos because certificates may be invalid since they are in the future
* Server logs are different so can't tell when something happened.  

So to make things right, we need to set the clocks. 

```
for i in $(seq 3); do ssh kubec-master-0$i sudo date +%T -s "09:41:00"; done
for i in $(seq 4); do ssh kubec0$i sudo date +%T -s "09:41:00"; done
```

(__Note__: If the date is off as well, then you'll need to run the ```date +%Y%m%d -s "20180917"``` in the for loop as well.)

Once the clocks are set, we need to set the hardware clock so it matches what is on the terminal.  That way when the system reboots the clock will match and be the same. 

```
for i in $(seq 3); do ssh kubec-master-0$i sudo hwclock -w; done
for i in $(seq 4); do ssh kubec0$i sudo hwclock -w; done
```

Always verify

```
for i in $(seq 3); do ssh kubec-master-0$i date; done
for i in $(seq 4); do ssh kubec0$i date; done
```

### Update our repositories

To make sure we can get the latest packages and that our system is up to date we run:

```
for i in $(seq 3); do ssh -t kubec-master-0$i "sudo apt update -y && sudo apt upgrade -y"; done
for i in $(seq 4); do ssh -t kubec0$i "sudo apt update -y && sudo apt upgrade -y"; done
```

Notice the ```-t``` in here as we will be prompted at times and need to respond. Since this goes serially you may want to open more windows up and expand them.  This can take a good chunk of time.  Not my favorite activity. 


#### NTP

Our time is pretty close, but let's get exact with NTP

Disable TimeSyncD time synchronization so we can use NTP. 
```
for i in $(seq 3); do ssh kubec-master-0$i sudo timedatectl set-ntp no; done
for i in $(seq 4); do ssh kubec0$i sudo tiemdatectl set-ntp no; done
```

```
for i in $(seq 3); do ssh kubec-master-0$i sudo apt install -y ntp; done
for i in $(seq 4); do ssh kubec0$i sudo apt install -y ntp; done

```

Verify NTP is running. 

```
for i in $(seq 3); do ssh kubec-master-0$i sudo systemctl status ntp; done
for i in $(seq 4); do ssh kubec0$i systemctl status ntp; done
```

This gets the dates all set and now we're happy with time. 



## Docker

### Installing Docker

```
for i in $(seq 3); do ssh -t kubec-master-0$i "sudo apt install -y docker.io"; done
for i in $(seq 4); do ssh -t kubec0$i "sudo apt install -y docker.io"; done
```


### Configuring Docker

#### Adding users to run Docker

Instead of typing ```sudo docker ...``` everytime we would like to make it so our default user is able to run docker commands.  

We can do this by adding the user to the docker group.  To do this, we go into the ```/etc/group``` file and append the name of the user to the ```docker``` group.  Open this file with 

```
sudo vi /etc/group
```

In the example below, the ```ubuntu``` user is added to the ```docker``` group: 

```
docker:x:982:ubuntu
```

After changing this, log out and log back in and the ```ubuntu``` user should now be able to run ```docker``` commands.  We do this individually with each host. 


From here we are ready to get Kubernetes installed on all the nodes. 

## Proxy


### ```apt```
If you are behind a proxy this is where we need to add proxy settings to ```apt``` so we can get packages from sites outside our datacenter.  For ```apt``` we need to update our proxy settings. 

Make a file called ```98proxy``` that contains the following: 

```
Acquire::https::Proxy "http://proxy.esl.cisco.com:80";
```
This has our https proxy settings. 

Copy this file to all the nodes: 

```
for i in $(seq 4); do scp 98proxy kubec0$i:/home/ubuntu/; done
for i in $(seq 4); do scp 98proxy kubec-master-0$i:/home/ubuntu/; done
```

Move it to the right directory: 

```
for i in $(seq 4); do ssh kubec0$i sudo mv /home/ubuntu/98proxy /etc/apt/apt.conf.d/; done
for i in $(seq 3); do ssh kubec-master-0$i sudo mv /home/ubuntu/98proxy /etc/apt/apt.conf.d/; done
```

### ```docker```

If you are behind a firewall you may need to add the proxy settings to your docker config.  Try testing: 

````
docker pull busybox
````

If it works, great!  No proxy required.  If it doesn't, time to update docker with the proxy settings!


```
for i in $(seq 4); do ssh kubec0$i sudo mkdir /etc/systemd/system/docker.service.d
```

Make a file called ```http-proxy.conf``` on your local machine.  The contents should be: 

```
[Service]
Environment="HTTPS_PROXY=http://proxy.esl.cisco.com:80"
Environment="NO_PROXY=localhost,127.0.0.1,10.99.104.44,10.99.104.124"
```

Where your proxy address and port are listed.  Let's copy this file to 
all the machines: 

```
for i in $(seq 3); do scp http-proxy.conf kubec-master-0$i:/tmp/; done
for i in $(seq 4); do scp http-proxy.conf kubec0$i:/tmp/; done
```

Next make the directory where they'll go: 

```
for i in $(seq 3); do ssh  kubec-master-0$i sudo mkdir -p  /etc/systemd/system/docker.service.d/; done
for i in $(seq 4); do ssh  kubec0$i sudo mkdir -p  /etc/systemd/system/docker.service.d/; done
```

Then move the proxy file to the correct directory:

```
for i in $(seq 3); do ssh  kubec-master-0$i sudo mv /tmp/http-proxy.conf /etc/systemd/system/docker.service.d/; done
for i in $(seq 4); do ssh  kubec0$i sudo mv /tmp/http-proxy.conf /etc/systemd/system/docker.service.d/; done
```

Now on each node, we need to reload the daemon and restart docker: 

```
for i in $(seq 3); do ssh  kubec-master-0$i "sudo systemctl daemon-reload; sudo systemctl restart docker"; done
for i in $(seq 4); do ssh  kubec0$i "sudo systemctl daemon-reload; sudo systemctl restart docker"; done
```

You should check that this worked by going to one of the nodes and getting a quick docker image: 

```
docker pull busybox
```
If you get errors, there may be an issue with the proxy file or some other setting. 


### Disable Swap

Kubernetes does not like swap so we need to turn it off. 

```
for i in $(seq 3); do ssh kubec-master-0$i sudo swapoff -a; done
for i in $(seq 4); do ssh kubec0$i sudo swapoff -a; done
```

Ideally when you install the OS you won't have any swap.  You can configure this by editing ```/etc/fstab``` 

```
UUID=6fc120d3-b0f8-4345-b685-ca7587d6a707 /               ext4    errors=remount-ro 0       1
/swapfile                                 none            swap    sw              0       0
```
By removing the last line and rebooting swap will be disabled permamently.  
