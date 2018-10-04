# Kubernetes in the Data Center

A Book for deploying Kubernetes systems on Bare Metal

* [Chapter 1: Kubernetes on Prem](chapters/01-OnPrem.md)

	1. Introduction
	1. Tradeoffs of OnPrem
	1. Tradeoffs of VMs vs. Bare Metal
	1. Tradeoffs of RYO vs. Buying
	1. Architecture Overview
	
* [Chapter 2: Hardware Configuration](chapters/02-bminstall.md)
	2. Networking Architecture and Design
	2. Nework configuration
	2. Server Architecture and Design
	2. Storage Architecture and Design
	2. OS Installation
* [Chapter 3: Linux Configuration](chapters/03-LinuxConfig.md)
	3. ```/etc/hosts```
	3. SSH Setup
	3. sudo
	3. hostnames
	3. Clocks and NTP
	3. Install and Configure Docker
	3. Testing Docker
	3. Swap
* [Kubernetes installation - Part 1 Server](chapters/04-KubernetesInstallation.md)
	4. Dependencies
	4. Load Balancing
	4. Kubeadm
	4. Installing Kubernetes Master Nodes
	4. Troubleshooting
	4. Adding Nodes
	
* [Kubernetes Installation - Part 2 Networking](chapters/05-networking.md)
	5. Overlay Networks: Channel, Calico, Flannel, Weave
	5. Installing Calico
	5. Verifying Cluster
	5. Installing MetalLB Load Balancing
	5. Cisco ACI for Network overlays

* [Kubernetes Installation - Part 3 HA Masters](chapters/05-hakubernetes)
	6. Adding in redundant master nodes
	6. Configuration changes
	6. Verifying changes
	6. Testing: busybox
	
* Kubernetes Storage
	7. Helm
	7. Rook
	7. Operators
	7. Minio
	7. Ceph
	7. Persistant Volumes and Volume Claims
	7. MySQL Application Example
	
* More Networking
	8. Networking Types
	8. Ingress Controllers: Traefik, Nginx, HA-Proxy
	8. Creating Ingress Rules
	8. Istio
	8. Istio Example Applications
* Kubernetes Monitoring
	9. Prometheus
	9. Kibana, Elastisearch, Fluentd, 
	9. Grafana
	9. App Dynamics
* OnPrem Security
	10. RBAC
	10. LDAP
	10. Harbor
	10. Umbrella
