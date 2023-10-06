#!/usr/bin/bash

# Script to initialize moto server; runs inside the motoserver container

# Launch moto server
moto_server --host 0.0.0.0 --port $MOTO_PORT & 

# Initialize data once server is ready
sleep 3 && curl -X POST "http://motoserver.czidnet:${MOTO_PORT}/moto-api/recorder/replay-recording"

# Go back to moto server
wait
