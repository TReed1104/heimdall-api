#!/bin/sh
echo ---------------------------------------
echo Deployment Start - Development
echo ---------------------------------------
echo Building and Deploying Flask API
echo ---------------------------------------
docker-compose -p flask-api-dev -f docker-compose.dev.yml up -d --build --remove-orphans
echo
echo ---------------------------------------
echo Conntainer Status:
echo ---------------------------------------
docker ps | grep 'flask-api'