# jaeger1.16-python-flask-envoy-k8s
This repository contains the files to install Jaeger 1.16 in to a K8s(tested in a 1.17.5 k8s) cluster, it also includes a Flask application that spans information to Jaeger, Jaeger is exposed through an ingress nginx or envoy using gloo
## How to use this repository
1. Clone the repository
```
git clone https://github.com/sergioarmgpl/jaeger1.16-python-flask-envoy-k8s.git
cd jaeger1.16-python-flask-envoy-k8s
```
2. Build your image choose between index.py or index_base.py and rename it as index.py
the image is supposed that use the jaeger installation in the observability namespace.  index.py file generates span and metrics and index_basic.py just span
```
cd python3-flask-traced/
mv index_base.py index.py #(If applies)
```
3. Edit the build.sh file with your username, please execute docker login and enter your credentials to push the image in a public repository the run the build.sh
```
/bin/bash build.sh or ./build
```
4. Push your image to docker hub
```
docker push user/image
```
5. Install your ingress controller, nginx or gloo(envoy)
6. Install jaeger operator
```
/bin/bash jaeger_install.sh
```
4. Install jaeger simplest installation
```
kubectl create -f simplest.yaml
```
5. Deploy the flask application, will be deployed in the default namespace
```
kubectl create -f jaeger-app.yaml
```
6. Expose your app with NodePort service type or as you want
```
kubectl expose deployment/jaeger-app --port=5000 --target-port=5000 --type=NodePort -n observability
```
7. Create the ingress rule to expose Jaeger UI
```
kubectl create -f ingress.yaml
```
Note: Uncomment your desired ingress
8. Enter to Jaeger
![Alt text](images/jaeger1.png?raw=true "Exec")
9. Access your app to generate some span in Jaeger
10. Choose in the Service dropdown my-traced-service o my-hello-service depending in the case
![Alt text](images/jaeger2.png?raw=true "Exec")

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
