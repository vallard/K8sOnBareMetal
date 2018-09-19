# Linux Configuration


## Docker

### Installing Docker

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

After changing this, log out and log back in and the ```ubuntu``` user should now be able to run ```docker``` commands. 