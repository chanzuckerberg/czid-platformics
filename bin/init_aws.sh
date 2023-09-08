#!/bin/bash

# ------------------------------------------------------------------------------
# Initialize mock AWS services
# ------------------------------------------------------------------------------

# Can't use `alias` unless in Bash's interactive mode, so using a function instead
function awslocal() {
    aws --endpoint-url=http://localhost:4000 "$@"
}

# Create dev bucket
awslocal s3 mb "s3://local-bucket"
