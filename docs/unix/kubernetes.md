# Kubernetes

[:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guides](../kubernetes/index.md)

### Installation

Install `kubectl` and `minikube` for local testing

````bash
# kubectl  
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"  
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl  

# minikube  
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64  
sudo install minikube-linux-amd64 /usr/local/bin/minikube  
minikube start --driver=docker  
````

### Essential Commands

| Category        | Command                                    | Description           |
| --------------- | ------------------------------------------ | --------------------- |
| **Pods**        | `kubectl get pods -A`                      | List all pods         |
|                 | `kubectl describe pod <name>`              | Inspect pod details   |
| **Deployments** | `kubectl rollout status deploy/<name>`     | Check deployment      |
|                 | `kubectl scale deploy/<name> --replicas=3` | Scale replicas        |
| **Services**    | `kubectl expose deploy/<name> --port=80`   | Create service        |
| **Debugging**   | `kubectl logs <pod> -f`                    | Stream logs           |
|                 | `kubectl exec -it <pod> -- sh`             | Enter container shell |
|                 |                                            |                       |

Sample Deployment (`deploy.yml`)

````yaml
apiVersion: apps/v1  
kind: Deployment  
metadata:  
  name: nginx  
spec:  
  replicas: 3  
  selector:  
    matchLabels:  
      app: nginx  
  template:  
    metadata:  
      labels:  
        app: nginx  
    spec:  
      containers:  
      - name: nginx  
        image: nginx:alpine  
        ports:  
        - containerPort: 80  
````

Apply

````bash
kubectl apply -f deploy.yml
````

### Tips

* Context Switching

````bash
kubectl config use-context <cluster-name>
````

* port forwarding

````bash
kubectl port-forward svc/nginx 8080:80
````

* resources limits

````bash
resources:  
  limits:  
    memory: "512Mi"  
    cpu: "1"  
````

#### Security Best Practices

* Use `Role-Based Access Control(RBAC)`
* Enable `Netowrk Policies`
* Scan images with `Trivy`

````bash
trivy image nginx:alpine
````

### Resources

* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
* [Minikube Docs](https://minikube.sigs.k8s.io/docs/)
* [Personal Notes](../kubernetes/index.md)