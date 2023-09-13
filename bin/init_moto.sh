#!/bin/bash

# Launch moto server
moto_server --host 0.0.0.0 --port $MOTO_PORT & 

# Initialize data
sleep 1 && curl -X POST http://localhost:4000/moto-api/recorder/replay-recording

# Go back to moto server
wait
