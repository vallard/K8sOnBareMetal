# Kubernetes in the Data Center

A Book for deploying Kubernetes systems on Bare Metal

* [Chapter 1: Kubernetes on Prem](chapters/01-OnPrem.md)
	* Introduction
	* Tradeoffs of OnPrem
	* Tradeoffs of VMs vs. Bare Metal
	* Tradeoffs of RYO vs. Buying
* [Chapter 2: Bare Metal configuration and OS installation](chapters/02-bminstall.md)
	* Node Configuration and Architecture
	* Disk space requirements
	* 
* [Chapter 3: Linux Configuration](chapters/03-LinuxConfig.md)
	* Install Docker
* [Kubernetes installation](chapters/04-KubernetesInstallation.md)
	* kubeadm
* [Chapter 4: Kubernetes Networking](chapters/05-networking.md)
	* Overlay Networks: Channel, Calico, Flannel, Weave
	* MetalLB Load Balancing

* [Chapter 5: HA Kubernetes](chapters/05-hakubernetes)
	* 

* More Networking
	* Ingress Controllers: Traefik, Nginx, HA-Proxy
	* Istio
* Kubernetes Storage
	* Rook
	* Operators
	* Minio
	* Ceph
* Kubernetes Monitoring
	* Prometheus
	* Kibana, Fluentd, ...
	* Grafana
	* App Dynamics in a Golang
* RBAC onPrem
	* LDAP
* Private Registry
	* Harbor
* Applications on Kubernetes
	* MySQL, PostgreSQL
