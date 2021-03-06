#use  ./build_jaeger.sh docker-user [advanced|basic]
#docker build --no-cache -t youruser/jaeger-app-flask .
export USER=$1
export TYPE=$2
rm index.py
cp index_jaeger_$TYPE.py index.py
docker build --no-cache -t $USER/jaeger-app-flask-metrics .
docker push $USER/jaeger-app-flask-metrics
