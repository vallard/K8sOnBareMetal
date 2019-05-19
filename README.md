# Kubernetes in the Data Center

A Book for deploying Kubernetes systems on Bare Metal

* [Chapter 1: Kubernetes on Prem](chapters/01-OnPrem.md)

	1. Course Introduction
	2. Understanding Kubernetes
	3. Planning Your Kubernetes Deployment   
		* Tradeoffs of OnPrem
		* Tradeoffs of VMs vs. Bare Metal
		* Tradeoffs of RYO vs. Buying
		* Our Architecture Overview
	
* [Chapter 2: Hardware Configuration](chapters/02-bminstall.md)
	
	2. Networking Architecture, Design, and Configuration
		* Video: Configure portchannel
	2. Storage Architecture and Design
	2. Server Architecture and Design
		* Video: Program CIMC, Firmware upgrade, RAID configuration
		* Video: OS Installation

		
* [Chapter 3: Linux Configuration](chapters/03-LinuxConfig.md)

	
	1. sudo (redo)
	1. networking (IP Address and networking constructs)
	1. SSH
	1. `/etc/hosts`
	1. hostnames
	1. Clocks and NTP
	1. Install and Configure Docker
	1. Testing Docker
	1. Swap
	
* [Chapter 4: Kubernetes installation](chapters/04-KubernetesInstallation.md)

	1. Dependencies
	1. Kubernetes Networking: Calico, Flannel, Weave, Cannel
	1. kubeadm 
	1. Install kubernetes networking
	1. Verify with busy box
	1. Installing MetalLB Load Balancing
	1. kubectl locally
	1. Kubernetes Web UI (Dashboard)
	1. Helm
	1. Cisco ACI for Container Networking
	1. Adding in redundant master nodes	
	
* [Chapter 5: Kubernetes Application Storage](chapters/07-storage)

	7. Ephemeral 
	8. Volumes basics
	9. NFS persistent volume 
	9. Persistant Volumes and Volume Claims
	7. MySQL Application Example
	7. Rook
	7. Operators
	7. Minio
	7. Ceph
	8. Backups
	
* [Chapter 6: Application Networking](chapters/08-networking)

	8. Networking Types (ClusterIP, NodePort, LoadBalancer)
	8. Ingress Controllers: Traefik, Nginx, HA-Proxy
	8. Creating Ingress Rules
	9. TLS
	8. Istio
	8. Istio Example Applications
	
* [Chapter 7: Running Kubernetes](chapters/x-things)
	1. Updating Applications
	2. CI/CD: Drone
	3. Batch and Cron Jobs
	4. Daemon Set
	2. Stateful Sets
	3. KubeFlow
	4. Autoscaling



* [Chapter 8: Kubernetes Monitoring](chapters/09-monitoring)

	9. Prometheus
	9. Kibana, Elastisearch, Fluentd, 
	9. Grafana
	9. Vendor Monitoring: App Dynamics, Others

* [Chapter 9: Security](chapters/10-security)

	10. RBAC
	10. LDAP
	10. Harbor
	10. Umbrella
