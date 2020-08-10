#use  ./build_pro.sh docker-user [advanced|basic]
#docker build --no-cache -t youruser/jaeger-app-flask .
export USER=$1
export TYPE=$2
rm index.py
cp index_pro_$TYPE.py index.py
docker build -t $USER/prometheus-example .
docker push $USER/prometheus-example
