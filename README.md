# Kubernetes on Bare Metal

A Book for deploying Kubernetes systems on Bare Metal

* [Chapter 1: Kubernetes on Prem](chapters/01-onprem.md)
	* Tradeoffs of OnPrem
	* Tradeoffs of VMs vs. Bare Metal
* [Chapter 2: Bare Metal configuration and OS installation](chapters/02-bminstall.md)
	* Node Configuration and Architecture
	* Disk space requirements
	* 
* [Chapter 3: Linux Configuration](chapters/03-LinuxConfig.md)
	* Install Docker
* Kubernetes installation
	* kubeadm
* Kubernetes Networking
	* Overlay Networks: Channel, Calico, Flannel, Weave
	* MetalLB Load Balancing
	* Ingress Controllers: Traefik, Nginx, HA-Proxy
	* Istio
* Kubernetes Storage
	* Rook
	* Operators
	* Minio
	* Ceph
* Kubernetes Monitoring
	* Prometheus
	* Grafana
	* App Dynamics in a Golang
* RBAC onPrem
	* LDAP
* Applications on Kubernetes
	* MySQL, PostgreSQL
