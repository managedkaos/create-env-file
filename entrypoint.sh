#!/bin/bash
set -e

# Default values
AWS_REGION=${AWS_REGION:-"us-east-1"}
PARAMETER_PATH=${PARAMETER_PATH:-""}

# Validate required parameters
if [ -z "$PARAMETER_PATH" ]; then
    echo "Error: PARAMETER_PATH environment variable is required"
    exit 1
fi

# Run the script with the parameters
exec python script.py --region "$AWS_REGION" --path "$PARAMETER_PATH"
