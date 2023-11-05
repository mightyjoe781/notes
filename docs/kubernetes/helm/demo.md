# Helm Demo



## Installing Bitnami Wordpress Helm Chart

````bash
minikube start

helm search hub wordpress -o yaml
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo list
helm repo update

helm search repo wordpress

helm install wordpress \
--set wordpressUsername=admin \
--set wordpressPassword=password \
--set mariadb.mariadbRootPassword=secretpassword \
bitnami/wordpress

helm list
kubectl get all
helm status wordpress
minikube service wordpress
navigate http://127.0.0.1:58388/wp-admin

helm uninstall wordpress
````







