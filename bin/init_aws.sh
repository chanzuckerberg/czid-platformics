#!/bin/bash

# ------------------------------------------------------------------------------
# Initialize mock AWS services
# ------------------------------------------------------------------------------

# Create dev bucket (vars defined in docker-compose file)
awslocal s3 mb "$S3_BUCKET_DEV"
