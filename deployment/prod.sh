#!/bin/sh
echo ---------------------------------------
echo Deployment Start - Production
echo ---------------------------------------
echo Building and Deploying Flask API
echo ---------------------------------------
docker-compose -p flask-api -f docker-compose.yml up -d --build --remove-orphans
echo
echo ---------------------------------------
echo Conntainer Status:
echo ---------------------------------------
docker ps | grep 'flask-api'