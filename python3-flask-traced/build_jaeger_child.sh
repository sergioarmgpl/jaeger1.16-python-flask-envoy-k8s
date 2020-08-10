#use  ./build_jaeger.sh docker-user [advanced|basic]
#docker build --no-cache -t youruser/jaeger-app-flask .
export USER=$1
rm index.py
cp index_jaeger_jaeger_child.py index.py
docker build -t $USER/jaeger-app-flask-metrics-child .
docker push $USER/jaeger-app-flask-metrics-child
