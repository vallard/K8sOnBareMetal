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

	3. sudo (redo)
	4. networking (IP Address and networking constructs)
	5. SSH
	6. `/etc/hosts`
	3. hostnames
	3. Clocks and NTP
	3. Install and Configure Docker
	3. Testing Docker
	3. Swap
	
* [Chapter 4: Kubernetes installation - Part 1 Server](chapters/04-KubernetesInstallation.md)

	4. Dependencies
	4. Load Balancing
	4. Kubeadm
	4. Installing Kubernetes Master Nodes
	4. Troubleshooting
	4. Adding Nodes
	
* [Chapter 5: Kubernetes Installation - Part 2 Networking](chapters/05-networking.md)

	5. Overlay Networks: Channel, Calico, Flannel, Weave
	5. Installing Calico
	5. Verifying Cluster
	5. Installing MetalLB Load Balancing
	5. Cisco ACI for Network overlays

* [Chapter 6: Kubernetes Verification](chapters/05-hakubernetes)

	6. Adding in redundant master nodes
	6. Configuration changes
	6. Verifying changes
	6. Testing: busybox
	
* [Chapter 7: Kubernetes Storage](chapters/07-storage)

	7. Helm
	7. Rook
	7. Operators
	7. Minio
	7. Ceph
	7. Persistant Volumes and Volume Claims
	7. MySQL Application Example
	
* [Chapter 8: More Networking](chapters/08-networking)

	8. Networking Types
	8. Ingress Controllers: Traefik, Nginx, HA-Proxy
	8. Creating Ingress Rules
	9. TLS
	8. Istio
	8. Istio Example Applications
	
* [Chapter X: Doing Kubernetes things](chapters/x-things)
	1. Batch and Cron Jobs
	2. Stateful Sets
	3. 


* [Chapter 9: Kubernetes Monitoring](chapters/09-monitoring)

	9. Prometheus
	9. Kibana, Elastisearch, Fluentd, 
	9. Grafana
	9. App Dynamics
* [Chapter 10: Security](chapters/10-security)

	10. RBAC
	10. LDAP
	10. Harbor
	10. Umbrella
