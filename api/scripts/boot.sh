#!/bin/sh

## Sleep to help mitigate the race condition on boot up
sleep 15s

## Start the app
exec gunicorn --bind 0.0.0.0:5000 main:app
