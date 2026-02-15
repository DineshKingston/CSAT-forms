#!/bin/bash

echo "=== Checking Current Container Status ==="
docker ps -a | grep clientpulse

echo -e "\n=== Checking Nginx Logs ==="
docker logs clientpulse_nginx --tail 50

echo -e "\n=== Checking if app container exists ==="
docker inspect clientpulse_app 2>&1 | head -20

echo -e "\n=== Attempting to restart app container ==="
# First, let's see if we can find the stopped container
APP_CONTAINER=$(docker ps -a --filter "name=clientpulse_app" --format "{{.ID}}" | head -1)

if [ ! -z "$APP_CONTAINER" ]; then
    echo "Found app container: $APP_CONTAINER"
    echo "Getting last logs before crash:"
    docker logs $APP_CONTAINER --tail 100
    
    echo -e "\n=== Restarting container ==="
    docker start $APP_CONTAINER
    sleep 5
    docker logs $APP_CONTAINER --tail 20
else
    echo "No app container found. Need to recreate it."
fi

echo -e "\n=== Checking Docker Network ==="
docker network ls
docker network inspect clientpulse_default 2>/dev/null || echo "Network not found"

echo -e "\n=== Testing connectivity between containers ==="
docker exec clientpulse_nginx ping -c 3 app 2>&1 || echo "Cannot ping app from nginx"

echo -e "\n=== Checking if port 8000 is being used ==="
netstat -tlnp | grep 8000 || ss -tlnp | grep 8000
