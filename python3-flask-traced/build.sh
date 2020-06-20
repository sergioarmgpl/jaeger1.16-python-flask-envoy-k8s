#docker build --no-cache -t youruser/jaeger-app-flask .
USER=czdev
docker build -t $USER/jaeger-app-flask-metrics .
docker push $USER/jaeger-app-flask-metrics
