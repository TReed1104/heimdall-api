#!/bin/sh
mkdir results

## Sleep to help mitigate the race condition on boot up
sleep 15s

## Run the testing scripts
nose2 --plugin nose2.plugins.junitxml -c configs/unittest.cfg

## If the tests pass, Start the app
exec gunicorn --bind 0.0.0.0:5000 main:app

## TODO: If fail exit 1
