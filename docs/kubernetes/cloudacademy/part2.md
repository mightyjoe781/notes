# Introduction to Kubernetes

## Pods

- basic building block in kubernetes
- container one or more container in a Pod
- Pod containers all share a container network
- one IP address per Pod
- since pod contains container, it includes all declarative properties for container
  - container image
  - container ports
  - container restart policy
  - resource limits
- desired properties written in manifest files

Example Manifest File

````yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mycontainer
    image: nginx:latest
````

- Manifests in Action
  - kubectl create sends manifest to Kubernetes API Server
  - API server does the following for Pod manifests
    - select a node with sufficient resource
    - schedule pod onto node
    - node pulls pod’s container image
    - starts pod’s container
- Manifests are useful
  - can be checked into source control
  - easy to share and work with

````bash
# first start the docker daemon (check docker documents)
# start minikube
minikube start

# check if kubectl is connected to API
kubectl get pods

# check yaml files from here : https://github.com/cloudacademy/intro-to-k8s
cat 1.1-basic_pod.yml
kubectl create -f 1.1-basic_pod.yml
kubectl get pods

# inspect the pod properties
kubectl describe pod mypod | more
# notice only 1 ip per pod and all containers share that IP

# let's attach a port to connect to pod # notice ports in container
cat 1.2-port_pod.yml

# NOTE : we cannot change ports on running pods thats why we need to delete the pod
kubectl delete pod mypod
kubectl create -f 1.2-port_pod.yml

# this should time out from host as cotnainers in pod can communicate inside only
curl 10.244.0.4:80

# there is a minikube trick to access this tho

# labels are important for selecting clusters for application
# we can use queue-control to only get nodes in us-east label
cat 1.3-labeled_pod.yml

# Notice QOS class is BestEffort
# pods are scheduled based on resources, here there is no guarantee of pod being up, it maybe evicted when resources are required by any other resource starved service
cat 1.4-labeled_pod.yml
# this sets resources request and memory limits to allow a guaranted uptime or it won't be scheduled until such resources are available
````

#### Minikube and ports magic

Method 1

- Expose the Pod via Service: `kubectl port-forward mypod 8080:80`

Method 2 (Explained in Details Ahead)

- Create a simple server deployment : `kubectl run hello-minikube --image=gcr.io/google_containers/echoserver:1.4 --port=8080`
- Expose this deployment : `kubectl expose deployment hello-minikube --type=NodePort`
- Check NodePort used by svc : `kubectl get svc hello-minikube`
- Find minikube IP : `minikube ip`
- Curl via : `curl minikube ip:<o_port>`
- Alternatively can use `minikube tunnel` to access on `localhost:8080`

## Services

- We are not able to reach the pods but even if we could what happens to ip when a pod restarts ? It changes then how we keep track of all this
- A service defines networking rules for accessing Pods in a cluster from internet
- Use labels to select a group of Pods
- services has fixed IP Address
- services can also distribute request across pods in the group

`````yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: webserver
  name: webserver
spec:
	# this service's target port
  ports:
  - port: 80
  # select every pod with app=webserver & expose them on port 80
  selector:
    app: webserver
  type: NodePort
`````

Execute: `kubectl create -f 2.1-web_service.yaml`

Get services : `kubectl get services`

````txt
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP        63m
webserver    NodePort    10.110.244.0   <none>        80:31657/TCP   4s
````

To get the node ip : `kubectl describe node | grep -i address -A 1` or `minikube ip`

Now we can connect to this webserver using : `<minicube_ip>:31657` 

NOTE : above works only for minikube running off of `qemu` driver

NOTE : for docker driver you need to use `minikube tunnel` or `minikube --port-forward svc/webserver 3000:80` Then visit localhost:8080 or localhost:3000 respectively

## Multi-Container Pods

Example Application :

- A simple counter application
- 4 containers split across 3 tiers
- application tier is a Node.js
- redis data tier storing the counter
- Poller/counter in the support tier
- All containers are using environment variables

### Kubernetes Namespaces

- Namespace separates resources according to users, environment or application
- RBAC can be used to secure access to namespace

````yaml
apiVersion: v1
kind: Namespace
metadata:
  name: microservice
  labels:
    app: counter
````

`````bash
# creating a namespace
kubectl create -f 3.1-namespace.yaml

# check the multi-container.yaml
cat 3.2-multi_container.yaml
# NOTE: By default pods pull latest image, this could cause problems if pod restart
# set a imagePullPolicy
kubectl create -f 3.2-multi_container.yaml -n microservice

kubectl get -n microservice pod app

kubectl logs -n microservice app counter --tail 10
kubectl logs -n microservice app poller -f
`````

## Service Discovery

Why Services 

- support multi-pod design
- provides static endpoint for each tier
- handles pod ip changes
- load balancing

### Service Discovery Mechanism

1. Environment Variables
   - Service address automatically injected in containers
   - environment vairables follow naming conventions based on service name
2. DNS
   - DNS records automatically created in cluster’s DNS
   - containers automatically configured to query cluster DNS

````bash
kubectl create -f 4.1-namespace.yaml

cat 4.2-data_tier.yaml
kubectl create -f 4.2-data_tier.yaml -n service-discovery
kubectl create -f 4.3-data_tier.yaml -n service-discovery
````

````yaml
apiVersion: v1
kind: Service
metadata:
  name: data-tier
  labels:
    app: microservices
spec:
  ports:
  - port: 6379
    protocol: TCP # default
    name: redis # optional when only 1 port
  selector:
    tier: data
  type: ClusterIP # default
# yaml trick to cram in multiple yaml files in one file
---
apiVersion: v1
kind: Pod
metadata:
  name: data-tier
  labels:
    app: microservices
    tier: data
spec:
  containers:
    - name: redis
      image: redis:latest
      imagePullPolicy: IfNotPresent
      ports:
        - containerPort: 6379
````

`````yaml
apiVersion: v1
kind: Service
metadata:
  name: app-tier
  labels:
    app: microservices
spec:
  ports:
  - port: 8080
  selector:
    tier: app
---
apiVersion: v1
kind: Pod
metadata:
  name: app-tier
  labels:
    app: microservices
    tier: app
spec:
  containers:
    - name: server
      image: lrakai/microservices:server-v1
      ports:
        - containerPort: 8080
      env:
        - name: REDIS_URL
          # Environment variable service discovery
          # Naming pattern:
          #   IP address: <all_caps_service_name>_SERVICE_HOST
          #   Port: <all_caps_service_name>_SERVICE_PORT
          #   Named Port: <all_caps_service_name>_SERVICE_PORT_<all_caps_port_name>
          value: redis://$(DATA_TIER_SERVICE_HOST):$(DATA_TIER_SERVICE_PORT_REDIS)
          # In multi-container example value was
          # value: redis://localhost:6379
`````

NOTE : Data Tier service must be created before app tier & must be present in namespace before referencing environment variables

FOR DNS Service Discovery

````yaml
apiVersion: v1
kind: Pod
metadata:
  name: support-tier
  labels:
    app: microservices
    tier: support
spec:
  containers:

    - name: counter
      image: lrakai/microservices:counter-v1
      env:
        - name: API_URL
          # DNS for service discovery
          # Naming pattern:
          #   IP address: <service_name>.<service_namespace>
          #   Port: needs to be extracted from SRV DNS record
          value: http://app-tier.service-discovery:8080

    - name: poller
      image: lrakai/microservices:poller-v1
      env:
        - name: API_URL
          # omit namespace to only search in the same namespace
          value: http://app-tier:$(APP_TIER_SERVICE_PORT)
````

Here its referenced by : label.namespace:PORT

Why did we split up our services into 3 files ? Because we want to later on scale the application but not the redis database
