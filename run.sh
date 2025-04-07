#!/bin/bash -xe
docker run \
    -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    -e AWS_REGION=${AWS_DEFAULT_REGION} \
    -e PARAMETER_PATH=${PARAMETER_PATH} \
    ghcr.io/managedkaos/create-env-file:main
