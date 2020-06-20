#docker build --no-cache -t youruser/jaeger-app-flask .
USER=czdev
docker build -t $USER/prometheus-example .
docker push $USER/prometheus-example
