# Introduction to Kubernetes

## Deployments

- We should not create pods directly and should be created via higher level construct like deployments
- Deployment represents multiple replicas of a pod
- Describes a desired state that Kuberenetes needs to achieve
- Deployment Controller master component converges actual state to desired state
- seamlessly supports scaling but scaling is best with stateless pods

````bash
kubectl create -f 5.1-namespace.yaml

kubectl create -n deployments -f 5.2-data_tier.yaml -f 5.3-app_tier.yaml -f 5.4-support_tier.yaml

kubectl get -n deployments deployments
kubectl get -n deployments pods
# NOTE: This doesn't scale the containesr
kubectl scale -n deployments deployments support-tier --replicas=5

# again get pods
kubectl get -n deployments pods

# destroy some replicas then watch
kubectl delete -n deployments pods support-tier-<hash1> support-tier-<hash2> support-tier-<hash3>
watch -n 1 kubectl -n deployments get pods
````

Data-Tier

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
---
apiVersion: apps/v1 # apps API group (higher level abstration are part of apps group)
kind: Deployment
metadata:
  name: data-tier
  labels:
    app: microservices
    tier: data
spec:
  replicas: 1		# copy of pod always running NOT CONTAINERS IN A POD
  selector:
    matchLabels:
      tier: data
  template:
    metadata:
      labels:
        app: microservices
        tier: data
    spec: # Pod spec
      containers:
      - name: redis
        image: redis:latest
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 6379
````

## Autoscaling

- scale automatically based on CPU Utilization (or custom metrics)
- set target CPU along with min and max replicas
- target CPU is expressed as a percentage of Pod’s CPU request
- kubernetes increases or decreases replicas according to load
- Defaults using CPU Usage
- Autoscaling depends on metrics being collected
- metric server is one solution for collecting metrics
- several manifest files are used to deploy Metric Server (https://github.com/kubernetes-sigs/metrics-server)

````bash
kubectl apply -f metrics-server/
kubectl top pods -n deployments

# 1000m = 1 cpu
kubectl apply -f 6.1-app_tier_cpu_request.yaml -n deployments
kubectl create -f 6.2-autoscale.yaml

watch -n 1 kubectl get -n deployments deployments
kubectl api-resources	# hpa is short-name
kubectl describe -n deployments hpa
kubectl get -n deployments hpa

kubectl edit -n deployments hpa		# opens vim to edit some config's and apply immidieately
````

````yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: app-tier
  labels:
    app: microservices
    tier: app
spec:
  maxReplicas: 5
  minReplicas: 1
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app-tier
  targetCPUUtilizationPercentage: 70

# Equivalent to
# kubectl autoscale deployment app-tier --max=5 --min=1 --cpu-percent=70
````

## Rolling Updates and Rollback

- Rollouts update Deployments changes like env variables

Rollout Strategy’s

- Rolling Update
  - default rollout strategy
  - update in groups rather than all-at-once
  - Both old and new version running for some time
  - alternate is recreate strategy
  - scaling is not a rollout
  - kubectl has commands to check, pause, resume, and rollback (undo) rollouts
- autoscaling and rollouts are compatible but to observe changes here first delete hpa

````bash
kubectl delete -n deployments hpa app-tier

kubectl edit -n deployments deployment app-tier
# change replica 2 to 10
# delete resources limits
watch -n1 kubectl get -n deployments deployment app-tier

# wait till its 10/10
kubectl edit -n deployments deployment app-tier
# check strategy defaults of 25%

# trigger rollout change image: name to smk under RestartPolicy
kubectl rollout -n deployments status deployment app-tier

# rollback :)
kubectl rollout -n deployments undo deployment app-tier
````

## Probes (HealthCheck)

### Readiness Probes

- check when a pod is ready to serve traffic/handle request
- useful after startup to check external dependencies
- readiness probes set the pod’s ready condition. Services only send traffic to Ready Pods

### Liveness Probes

- Detect when a pod enters a broken state
- kubernetes will restart the pod for you
- declared in the same way as readiness probes
- Probes can be declared in Pod’s containers
- all container probes must pass for the Pod to pass
- probe actions can be a command that runs in the container, an HTTP GET request, or opening a TCP socket
- by default probes check containers every 10 seconds

Data Tier (redis)

- Liveness : Open TCP socket
- Readiness: redis-cli ping command

App Tier (server)

- liveness: HTTP GET /probe/liveness
- Readiness: HTTP GET /probe/readiness

````bash
kubectl create -f 7.1-namespace.yaml
diff -y 5.2-data_tier.yaml 7.2-data_tier.yaml
> output
								>                   name: redis
								>               livenessProbe:
								>                 tcpSocket:
								>                   port: redis # named port
								>                 initialDelaySeconds: 15
								>               readinessProbe:
								>                 exec:
								>                   command:
								>                   - redis-cli
								>                   - ping
								>                 initialDelaySeconds: 5
> end of output

# it is suggested to have more delay to liveness & it requires 3 fails to trigger restart
kubectl create -f 7.2-data_tier.yaml -n probes
kubectl get deployments -n probes -w

diff -y 5.3-app_tier.yaml 7.3-app_tier.yaml
								>                 - name: DEBUG
								>                   value: express:*
								>               livenessProbe:	# dummy always return 200 OK
								>                 httpGet:
								>                   path: /probe/liveness
								>                   port: server
								>                 initialDelaySeconds: 5
								>               readinessProbe:	# data-tier is available
								>                 httpGet:
								>                   path: /probe/readiness
								>                   port: server
								>                 initialDelaySeconds: 3
								
kubectl create -f 7.3-app_tier.yaml -n probes
kubectl get -n probes pods
kubectl logs -n probes app-tier-<hashid> | cut -d' ' -f5,8 
````

## Init Containers

- Sometimes you need to wait for a service, downloads, dynamic or decisions before starting a Pod’s container
- prefer to separate initialization wait logic from the container image
- initialization is tightly coupled to the main application (belongs in the pod)
- init containers allow you to run initialization tasks before starting the main container(s)

Init Container:

- pods can declare any number of init containers
- Init containers run in order and to completion
- use their own images
- easy way to block or delay starting an application
- run every time a pod is created (liveness fails) (runs atleast once)

NOTE : init containers do not have readiness Probe

````bash
diff -y 7.3-app_tier.yaml 8.1-app_tier.yaml
								>             initContainers:
								>               - name: await-redis
								>                 image: lrakai/microservices:server-v1
								>                 env:
								>                 - name: REDIS_URL
								>                   value: redis://$(DATA_TIER_SERVICE_HOST):$(DA
								>                 command:
								>                   - npm
								>                   - run-script
								>                   - await-redis
								
kubectl create -n probes -f 8.1-app_tier.yaml
kubectl get pods -n probes
kubectl describe pod app-tier-<hash> -n probes

kubectl logs -n probes app-tier-<hash> -c await-redis
````

`npm run-script await-redis` script waits till there is a connection with redis
