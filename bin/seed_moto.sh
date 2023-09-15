#!/bin/bash

# Script to seed moto server; runs outside the motoserver container for development

aws --endpoint-url=http://localhost:4000 s3 mb s3://local-bucket
