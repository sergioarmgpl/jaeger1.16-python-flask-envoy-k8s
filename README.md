# jaeger1.16-python-flask-envoy-k8s
This repository contains the files to install Jaeger 1.16 in to a K8s(tested in a 1.17.5 k8s) cluster, it also includes a Flask application that spans information to Jaeger, Jaeger is exposed through an ingress nginx or envoy using gloo
## requirements
1. Install Docker  
2. Install helm  
3. Install kubectl  
## How to use this repository
1. Clone the repository
```
git clone https://github.com/sergioarmgpl/jaeger1.16-python-flask-envoy-k8s.git
cd jaeger1.16-python-flask-envoy-k8s
```
## Installing your cluster with k3s (Optional)
1. Create an instance in your prefered cloud and execute the next command to install k3s
```
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--tls-san PUBLIC_IP --node-external-ip PUBLIC_IP" sh -s -
```
This command will install your cluster in AWS/GCP/Azure you dont have to specify the external-ip if you are using Digital Ocean  
2. The extract the config yaml to connect to the cluster using kubectl, for that you have to copy the file /etc/rancher/k3s/k3s.yaml in your k3s cluster, and copy that in your local computer in the ~/.kube/config file to have access to your cluster  

## Deploying Jaeger and your demo apps to do some tracing
1. Build your app1 and app2 docker images and deploy it to Docker Hub using the
scripts located in python3-flask-traced
```
cd python3-flask-traced
docker login [Enter yourDockerUser and password]
./build_jaeger.sh yourDockerUser advanced
./build_jaeger_child.sh yourDockerUser
```
And that it.
3. Return to jaeger1.16-python-flask-envoy-k8s directory and deploy jaeger with helm, using the next commands:
```
cd ..
kubectl create ns observability  
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts  
helm install jaeger jaegertracing/jaeger \  
  --set provisionDataStore.cassandra=false \  
  --set provisionDataStore.elasticsearch=true \  
  --set storage.type=elasticsearch \  
  --set spark.enabled=true \  
  --set spark.schedule="*/1 * * * *"  \  
  --set elasticsearch.minimumMasterNodes=1 \  
  --set elasticsearch.replicas=1 \  
  -n observability  
```  
This will deploy a minimal setup for production, you can install jaeger with Jaeger Operator with the AllInOne image, but this will not create your DAG graph in jaeger, to activate the DAG you need the spark in your installation  .
4. Deploy the apps with the next commands, you have to change the user in the deployment part to match it with your user. Change the code of the apps only if the services doesnt match with the current hosts in the python files, for example, if you use the Jaeger Operator you can spect to find something like simplest-query services.
```
kubectl create -f jaeger-app.yaml
kubectl create -f jaeger-app-2.yaml
```
5. Check for the different services created to access the apps
```
kubect get services -n observability
```
6. Expose jaeger locally with the next commands:
```
export POD_NAME=$(kubectl get pods --namespace observability -l "app.kubernetes.io/instance=jaeger,app.kubernetes.io/component=query" -o jsonpath="{.items[0].metadata.name}")
  echo 
```
```
kubectl port-forward --namespace observability $POD_NAME 8080:16686
```
7. Access the panel in your browser with the next url:  
```
http://127.0.0.1:8080/
```
8. Enter to Jaeger
![Alt text](images/jaeger1.png?raw=true "Exec")
9. Access your app to generate some span in Jaeger
10. Choose in the Service dropdown and try to find your traced service, after you generate some traces accessing this apps in the browser
![Alt text](images/jaeger2.png?raw=true "Exec")

## Extra configuration
You can check for additional files in this repo to use an ingress configuration to have access to Jaeger  
```
kubectl create -f ingress.yaml
```
Note: Uncomment your desired ingress


Enjoy it!
## Coming up
The next release will include the metrics in Prometheus

## Ingress Notes
install nginx-ingress with helm for quickstart
install gloo ingress with this link: https://docs.solo.io/gloo/1.1.0/installation/ingress

## References
1. https://opentelemetry-python.readthedocs.io/en/stable/getting-started.html
2. https://www.jaegertracing.io/docs/1.16/operator/
3. https://docs.solo.io/gloo/1.1.0/installation/ingress
4. https://rancher.com/docs/k3s/latest/en/installation/install-options/server-config/  
5. https://github.com/jaegertracing/helm-charts/tree/master/charts/jaeger