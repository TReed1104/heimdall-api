#!/bin/sh
echo ---------------------------------------
echo Deployment Start - Testing
echo ---------------------------------------
echo Building and Deploying Heimdall API
echo ---------------------------------------
docker-compose -p heimdall-api-testing -f docker-compose.test.yml up -d --build --remove-orphans
echo
echo ---------------------------------------
echo Conntainer Status:
echo ---------------------------------------
docker ps | grep 'heimdall-api'