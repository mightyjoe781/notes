# Amazon EKS Networking

## Kubernetes Architecture

![](assets/Pasted%20image%2020251030133150.png)

- Kubernetes Cluster consists of Control Plane and Data Plane
- Control plane consists of set of control processes hosted on master nodes
- Data plane consist of set of worker nodes called Nodes
- Nodes host the Pods
- A Pod represents a group of one or more application containers

![](assets/Pasted%20image%2020251030133213.png)

### Control Plane Components

- kube-apiserver
    - exposes kubernetes APIs. It's a frontend for the Kubernetes Control Plane
- etcd
    - key-value store used as Kubernetes backing store for all cluster data
- kube-scheduler
    - Watches for newly created Pods with no assigned node, and selects a node for them to run on.
- kube-controller-manager
    - Runs controller processes such as Node controller, Replication controller, Namespace controller, Job Controller, EndpointSlice controller etc.
- cloud-controller-manager
    - Links Kubernetes cluster into cloud provider's API such as Node controller for determining if node (instance) is deleted in the cloud, Service controller for cloud load balancer etc.

### Data Plane Components

- Node
    - hosts the pods (applications)
- kubelet
    - An agent that runs on each node in the cluster. It makes sure that containers are running in a Pod.
- kube-proxy
    - Enables network communication to Pods from network sessions inside or outside of your cluster
- Container Runtime
    - Responsible for running containers. Kubernetes supports container runtimes such as containerd, CRI-O, and any other implementation of the Kubernetes CR

### Application Deployment to Kubernetes

![](assets/Pasted%20image%2020251030133708.png)

## AWS EKS Architecture

### Control Plane & Data Plane in AWS

![](assets/Pasted%20image%2020251030134250.png)

![](assets/Pasted%20image%2020251030134307.png)

### EKS - Data Plane Hosting Options

![](assets/Pasted%20image%2020251030134341.png)

## AWS EKS Cluster Networking

![](assets/Pasted%20image%2020251030135032.png)

- EKS Control Plane is launched in AWS managed account & VPC
- Data Plane nodes are launched in Customer account & VPC
- EKS Provisions 2-4 ENIs in the Customer VPC to enable the communication between Control Plane and VPC.
- It's recommended to have separate subnets for EKS ENIs, EKS needs atleast 6 IPs in each subnet (16 recommended)
- EKS creates and associates SG to these EKS owned ENIs (and also to Managed Groups Nodes)
- Kubernetes API Server can be accesses over the internet (by default)
- EKS allows assigning IPv4 or IPv6 IP addresses to Pods (but not in dualstack mode)

### EKS cluster endpoint access - Public (default)
![](assets/Pasted%20image%2020251030135254.png)
### EKS Cluster Endpoint Access - Public & Private
![](assets/Pasted%20image%2020251030135305.png)
### EKS Cluster Endpoint Access - Private
![](assets/Pasted%20image%2020251030135242.png)
### EKS API Private access through PrivateLink
![](assets/Pasted%20image%2020251030135230.png)
### EKS VPC extended connectivity

![](assets/Pasted%20image%2020251030135326.png)

## EKS Pod Networking

### Kubernetes Network Model

- CNCF Networking specifications
- Every pod gets its own IP address
- Containers in the same Pod share the network IP Address
- All pods can communicate with all pods without using NAT
- All nodes can communicate with all pods without NAT
- The IP that a pod sees itself as is the same IP that other see it as

### Amazon VPC CNI Plugin

![](assets/Pasted%20image%2020251030143022.png)

- Amazon VPC Container Network Interface (CNI) plugin
    - creates and attached ENIs to worker nodes
    - Assigns ENI secondary IP addresses to Pods
- Amazon EKS officially supports the Amazon VPC CNI plugin for Kubernetes
- Alternate compatible CNI plugins
    - Tigera ~ Calico
    - Isovalent ~ Cillium
    - Weaveworks ~ Weave Net
    - VMware ~ Antrea

Max Pods = (Total number of network interfaces) x (Maximum IPs per network interface - 1) + 2

Example (m5.large with IPv4 address) : 
Max Pods = 3 x (10-1) + 2 = 29

Above number of pods seems to less, so AWS provides special nodes.

#### Only AWS Nitro-based nodes use this capability

Prefix delegation:
Assign a prefix to EC2 ENI

- `/28` block for IPv4 ( x16)
- `/80` block for IPv6 (x280 trillion)

Example (m5.large with IPv4 address):
Max Pods = 3 x (10-1) x 16 + 2 = 434

*Max Pods(recommended) = 110*

### Assigning IPv6 addresses to pods and services

![](assets/Pasted%20image%2020251030145059.png)

- By default, Kubernetes assigns IPv4 addresses to pods and services but we can also configure cluster with IPv6 addresses.
- EKS doesn’t support dual-stack pods or services.
- For Amazon EC2 nodes, you must configure the Amazon VPC CNI add-on with IP prefix delegation and IPv6.
- You must also assign IPv4 address to VPC and subnets as VPC does require IPv4 addresses to function.
- Subnets must have auto-assign IPv6 address enabled.
- Not supported for Windows pods and services.

### Pod to Pod communication

![](assets/Pasted%20image%2020251030145128.png)

### Amazon EKS Pod Network - traffic between Pod and external network

![](assets/Pasted%20image%2020251030145827.png)

- When a pod communicates to any IPv4 address that isn't within a CIDR block of VPC, the Amazon VPC CNI plugin translates the pod's IPv4 address to the primary private IPv4 address of the primary ENI of the node that the pod is running on
- For IPv6 address family, this isn't applicable, because IPv6 addresses are not network translated

### Pod to external network communication - Node in Public Subnet
![](assets/Pasted%20image%2020251030150122.png)

### Pod to external network communication - Node in Private Subnet
![](assets/Pasted%20image%2020251030150112.png)
### External network to Pod Communication
![](assets/Pasted%20image%2020251030150102.png)
### Multi-homed Pods with Multus CNI

![](assets/Pasted%20image%2020251030150006.png)

- Enables attaching multiple interface to pods
- With Multus you can create a multi-homed pod that has multiple interface
- AWS support for Multus comes with VPC CNI

## Security Groups in EKS

![](assets/Pasted%20image%2020251030151617.png)

- When you create EKS Cluster, it creates and associates SG with following rules

![](assets/Pasted%20image%2020251030151602.png)

- EKS associates this SG with
    - ENIs created by EKS in Customer VPC
    - ENIs of the nodes in Managed Node group
- At minimum following Outbound rules are required

![](assets/Pasted%20image%2020251030151545.png)

### Pod Security Groups - The problem

![](assets/Pasted%20image%2020251030151707.png)

- SG is assigned to Node ENIs and hence all Pods having secondary IPs from the same ENI will use the same SG
- This is a drawback if you need different security groups for different Pods
- One of the option is to use Network policy engine like Calico which provides network security policies to restrict inter pod traffic using iptables
- EKS native option is to use Trunk and Branch ENIs

### The solution Trunk and Branch ENIs

![](assets/Pasted%20image%2020251030151931.png)

- Amazon EKS and ECS supports Trunk & Branch ENI feature
- A VPC resource controller add-on named “amazon- vpc-resource-controller-k8s” manages Trunk & Branch Network Interfaces
- When ENABLE_POD_ENI=true, VPC resource controller creates special network interface called a trunk network interface with description “aws-k8s- trunk-eni” and attaches it to the node
- The controller also creates branch interfaces with description "aws-k8s-branch-eni" and associates them with the trunk interface.
- Each Pod gets dedicated ENI (branch ENI) mapped to trunk ENI
- Independent Security group per Pod Note
- Security groups for pods can't be used with Windows nodes
- If cluster is using IPv6 address family then this feature only works with Fargate nodes
- Supported by most Nitro based system (t instance family is not supported)
- The Node instances should be listed in limits.go file with IsTrunkingCompatible: true

![](assets/Pasted%20image%2020251030152024.png)

## Exposing Services using ClusterIP, NodePort, LoadBalancer & Ingress

### Kuberenetes Service

- Accessing applications by their Pod’s IPs is usually an anti-pattern because
    - Pods are non-permanent objects
    - Pods may be created and destroyed
    - Pods move between the cluster’s nodes due to a scaling event, a node replacement, or a configuration change.
- Kubernetes Service is a way to expose an application running on a set of Pods as a network service
- Kubernetes & EKS Supports following Service Types:
    - ClusterIP (access services from inside EKS cluster using Virtual IP)
    - NodePort (access services externally using Node static port)
    - LoadBalancer (Network load balancing, access services externally using CLB/NLB Layer4)
    - Ingress (Application load balancing, access services externally using ALB Layer7)
### ClusterIP

![](assets/Pasted%20image%2020251030203602.png)

- ClusterIP is the default service type
- Makes the service reachable/accessible only from within the cluster
- Service is exposed on a virtual IP on each node. This IP is not exposed outside of a cluster.
- The service virtual IP is assigned from a pool which is configured by setting following parameter in `kube-apiserver`: `--service-cluster-ip-range`
- If not configured explicitly then Amazon EKS provisions either 10.100.0.0/16 or 172.20.0.0/16 for this Virtual IP.
- A `kube-proxy` daemon on each cluster node defines the ClusterIP to Pod IP mapping in iptables rules
• Service is accessible with private DNS `<service-name>.<namespace-name>.svc.cluster.local`

### NodePort

![](assets/Pasted%20image%2020251030203654.png)

- NodePort is used to make a Kubernetes service accessible from outside the cluster
- Exposes the service on each worker node's IP at a static port, called the NodePort
- One Node port per Service
- Port range: 30000-32767
- NodePort internally uses ClusterIP to route the NodeIP/Port requests to ClusterIP service
- Client needs to keep track of Node IPs and any IP changes over the time
- Not a feasible option to expose services to the outside world

### EKS Network & Application Load Balancing

- ServiceType=LoadBalancer
    - Handled by Kubernetes Controller Manager (in-tree cloud controller)
    - Deploys AWS CLB (default) or NLB in instance mode
    - Layer 4 with NLB and Layer 4/7 with CLB
    - Now also supported by newer controller called AWS Load Balancer Controlle
- ServiceType=Ingress
    - Handed by AWS Load Balancer Controller (formerly AWS ALB Ingress controller)
    - Deploys ALB in Instance & IP mode for ingress resource
    - Layer 7

### Load Balancer Service (with Legacy Controller)

![](assets/Pasted%20image%2020251030205730.png)

- Exposes services to the client outside of the cluster
- LoadBalancer service is built on top of NodePort service
- Supports:
    - Classic Load Balancer (CLB)
        - Layer 4/Layer 7 traffic (TCP, SSL/TLS, HTTP, HTTPS)
    - Network Load Balancer (NLB)
        - Layer4 traffic (TCP, UDP, TLS)
        - Instance mode only
### LoadBalancer Service (with newer controller)

![](assets/Pasted%20image%2020251030205854.png)

- Recommended to use AWS Load Balancer Controller
- For target as IP (for EC2 or Fargate) use:
![](assets/Pasted%20image%2020251030205829.png)
- For target as Instance (for EC2) use:
![](assets/Pasted%20image%2020251030205841.png)
- Each service needs a dedicated NLB
- Scaling & management is a challenge when number of services grows

### Kubernetes Ingress

![](assets/Pasted%20image%2020251030205912.png)

- Exposes services to the client outside of the cluster
- Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster.
- Traffic routing is controlled by rules defined on the Ingress resource.
- Saves cost and complexity as multiple services can be added behind a single ALB using ALB target groups.
- EKS uses AWS Load Balancer Controller for provisioning load balancer resources

### AWS Load Balancer Controller

![](assets/Pasted%20image%2020251030210026.png)

- The AWS implementation for Ingress controller
- Translates the Ingress rules, parameters, and annotations into the ALB configuration, creating listeners and target groups and connecting their targets to the backend Services.
- Supports target as Instance or Pod IP.
- Annotation used: `kubernetes.io/ingress.class: alb`
- Share ALB with multiple services by using annotation: `alb.ingress.kubernetes.io/group.name: my-group`
- Traffic for IPv6 is supported for IP targets only. Use annotation: `alb.ingress.kubernetes.io/ip-address-type: dualstack`

![](assets/Pasted%20image%2020251030205923.png)
### Preserving Client IP

![](assets/Pasted%20image%2020251030205104.png)

- For NLB with LoadBalancer service
    - externalTrafficPolicy service spec defines how load-balancing happens in the cluster
    - If external TrafficPolicy=Cluster, the traffic may be sent to another node and source IP is changed to node's IP address thereby Client IP is not preserved. However load is evenly spread across the nodes.
    - By setting external TrafficPolicy=Local, traffic is not routed outside of the node and client IP addresses is propagated to the end Pods. This could result in uneven distribution of traffic.
- For ALB Ingress service
    - HTTP header X-Forwarded-For is used to get the Client IP

## EKS Custom Networking - Extending IPv4 address space

![](assets/Pasted%20image%2020251030155153.png)

- Problem
    - If you have limited IP space, it will constraint the number of Pods
    - /24 CIDR will have 251 unique IPv4 addresses

### Custom Networking

- Add Secondary VPC CIDR in the range 100.64.0.0/16 (~65000 IPs) to the VPC
- This CIDR IP addresses are routable only within the VPC
- Enable VPC CNI Custom Networking
- VPC CNI plugin creates Secondary ENI in the separate subnet
- Only IPs from Secondary ENI are assigned to Pods
- Custom Networking can be combined with SNAT

![](assets/Pasted%20image%2020251030155302.png)

![](assets/Pasted%20image%2020251030155316.png)
