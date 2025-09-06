# Kubernetes Patterns for Application Developers

[Resource Repo](https://github.com/lrakai/kubernetes-patterns-for-application-developers)

## Multi-Container Patterns

#### Why Pods ?

- pods are abstraction above containers but why ?
- Kubernetes needs additional information
- simplifies using different underlying container runtimes like docker or rocket
- co-locate tightly coupled containers without packaging them as a single image

Patterns

### Sidecar Pattern

- uses a helper container to assist a primary container
- commonly used for logging, file syncing, watchers
- benefit inlcude leaner main container, failure isolation, independent update cycles
- File Sync Sidecar Example
    - primary container : web-server, sidecar : content puller
    - content puller & web-server share a single volume within pod, in which content puller fetches latest files from CMS and keeps both containers in sync via volume.

### Ambassador Pattern

- ambassador container is a proxy for communicating to and from the primary container
- commonly used for communicating with databases
- streamlined development experience, potential to reuse ambassador across language
- Database Ambassador Example:
    - primary container : web-app
    - ambassador : database-proxy
    - web app handles request
    - database requests are sent to database proxy over localhost
    - database proxy then forwards the requests to appropriate database
    - possibly sharding the request

### Adaptor Pattern

- adapter present a standardized interface across multiple pods
- commonly used for normalizing output logs and monitoring data
- adapts third-party software to meet your needs

Example Changes logging format from txt to json

````yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapted-pod
spec:
  containers:
  - name: app
    image: alpine:3.9.2
    command: ["/bin/sh", "-c"]
    args:
    - while true; do 
        date > /metrics/raw.txt;
        top -n 1 -b >> /metrics/raw.txt;
        sleep 5;
      done
    # Share metric data between containers
    volumeMounts:
    - name: metrics
      mountPath: /metrics
  - name: adapter
    image: httpd:2.4.38-alpine
    command: ["/bin/sh", "-c"]
    # Adapt the legacy output to standard monitoring format
    args:
    - while true; do 
        date=$(head -1 /metrics/raw.txt);
        memory=$(head -2 /metrics/raw.txt | tail -1 | grep -o -E '\d+\w' | head -1);
        cpu=$(head -3 /metrics/raw.txt | tail -1 | grep -o -E '\d+%' | head -1);
        echo "{\"date\":\"$date\",\"memory\":\"$memory\",\"cpu\":\"$cpu\"}" > /metrics/adapted.json;
        sleep 5;
      done
    # Share metric data between containers
    volumeMounts:
    - name: metrics
      mountPath: /metrics
  volumes:
  - name: metrics
    emptydir:
````



## Networking

### Networking Basics

- each pod has one unique IP, while all containers inside pod share this one IP and communicate with each other freely
- Networking Plugins enables Pod to Pod Communication

### Services

- maintains a service replica pods selected based on labels to keep track of the pod during pods lifetime
- maintains a list of endpoints as pods are added and removed from the set
- can send request to any pod in the set
- clients of service only need to know about the service rather than specific pods
- pods can discover services via environment variables as long they are created after service or by using DNS Addon and IP Resolution
- ClusterIP service is only reachable within cluster. Kubeproxy cluster component that runs on each node is responsible for proxying the request for the service to one of the services endpoint.
- NodePort service allows any port to be open outside the cluster
- LoadBalancer Service exposes the service externally through a cloud providers load balancer. Also creates ClusterIP and NodePort
- External Name : external service enabled by DNS, used for Database as a Service or other things

### Network Policy

- Rules for controlling network access to Pods
- Similar to security groups controlling access to virtual machines
- scoped to namespace
- Caveat
    - kubernetest network plugin must support network policy
    - example : calico, canal, flannel etc.
- Non-isolated pod : accepts traffic from anywhere
- Isolated pods are non-isolated pods once selected by network policy

````yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-us-east
  namespace: network-policy
spec:
  # Which Pods the policy applies to
  podSelector:
    matchLabels:
      app: server
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    # Supports podSelector, namespaceSelector, and ipBlock
    - podSelector:
        matchLabels:
          region: us-east
    ports: # If not present allows all ports 
    - protocol: TCP
      port: 8888
  egress:
  - to: # Allows all traffic when empty
````

Block one-IP

````yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-one-ip
  namespace: network-policy
spec:
  podSelector:
    matchLabels:
      app: server
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0			# all ips
        except:
        - 192.168.134.71/32
````

## Service-Accounts

### Service Accounts

- provide an identity to Pods in the cluster
- stored in, and managed by the cluster
- scoped to namespace
- service account are compatible with RBAC(Role-Based Access Control)
- pods have a token mounted on a volume that can be used to authenticate requests
- default service account token has no additional permission than an unauthenticated user

### Configuration

````bash
# kube api service accounts
kubectl get -n kube-system serviceaccounts | more

# finding roles in coredns serviceaccount
kubectl describe -n kube-system clusterrole system:coredns
````

### Image Pull Secrets

- image pull secrets authenticate with private container registries
- service accounts can also store image pull secrets

## Leveraging kubectl

#### Shell Completion

- get all commands: `kubectl | more`
- get all completion commands: `kubectl completion --help`
- enable completion in shell: `source <(kubectl completion bash)` (Add to .bashrc for enabling it every login)
- Now `kubectl <TAB>` should work. Try : `kubectl get <TAB>`
- with completion enabled you can even autocomplete resource types but you can use short names
- To get entire list of completion : `kubectl api-resource`

#### get Tricks

- getting specific pods with labels : `kubectl get pods --all-namespace -L <label_name> -l [filter_label_name]`
- sort by the fields : `kubectl get pods -n kube-system --sort-by=metadata.creationTimestamp` or more correctly`kubectl get pods -n kube-system --sort-by='{.metadata.creationTimestamp}`
- output yaml for get commands: `kubectl get pods -n kube-system kube-proxy-<hash> --output=yaml`
- To print ip and sort by ip: `kubectl get pods -n kube-system --sort-by='{.status.podIP}' -o wide`

#### Generating Manifests

- creating resources without manifests: `kubectl create -h | less`
- try creating namespace : `kubectl create namespace tips -o yaml --dry-run`
- Redirect output to mkdir tips : `kubectl create ns tips -o yaml --dry-run > tips/1-namespaec.yaml`
- Create a nginx deployments : `kubectl run nginx --image=nginx --port=80 --replicas=2 --expose --dry-run -o yaml`
- exporting a resource: `kubectl get pods -n kube-system kube-proxy-<hash> -o yaml --export`

#### Explaining Fields

- `kubectl explain -h | less`
- to get information about a fields : `kubectl explain pod | more`
- more information : `kubectl explain pod.spec.containers.resources | more`

