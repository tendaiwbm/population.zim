cd ddl-scripts/
sh setup-db.sh
cd ..

docker rm APIQgis
docker rmi api:2
docker build -f ../config/APIDockerfile -t api:2 ../config/
docker run -d --name=APIQgis -p 8001:8001 --mount type=bind,source=/home/tendaiwbm/zviitwa/dB/populationZim/v2/api,target=/app api:2
docker stop APIQgis

docker rm SRVRNginx
docker rmi server:2
docker build -f ../config/SRVRDockerfile -t server:2 ../config/
docker run -d --name=SRVRNginx -p 8081:80 --mount type=bind,source=/home/tendaiwbm/zviitwa/dB/populationZim/v2,target=/app server:2
docker exec SRVRNginx sh -c "cp /app/config/server/nginx.conf /etc/nginx/nginx.conf; cp /app/config/server/uwsgi_params /etc/nginx/uwsgi_params"
docker stop SRVRNginx

