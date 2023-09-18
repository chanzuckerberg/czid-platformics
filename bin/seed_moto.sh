#!/bin/bash

# Script to seed moto server; runs outside the motoserver container for development

aws="aws --endpoint-url=http://localhost:4000"
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_REGION=us-west-2
$aws s3 mb s3://local-bucket
