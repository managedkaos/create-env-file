#!/usr/bin/env python3
"""
Script to read parameters from AWS Parameter Store and output them in .env format.
"""

import sys
import boto3
import argparse
from typing import List, Dict


def get_parameters(region: str, path: str) -> List[Dict]:
    """
    Fetch parameters from AWS Parameter Store.

    Args:
        region: AWS region
        path: Parameter Store path

    Returns:
        List of parameter dictionaries
    """
    ssm = boto3.client('ssm', region_name=region)

    parameters = []
    next_token = None

    while True:
        kwargs = {
            'Path': path,
            'Recursive': True,
            'WithDecryption': True
        }

        if next_token:
            kwargs['NextToken'] = next_token

        response = ssm.get_parameters_by_path(**kwargs)
        parameters.extend(response['Parameters'])

        next_token = response.get('NextToken')
        if not next_token:
            break

    return parameters


def format_env_output(parameters: List[Dict]) -> str:
    """
    Format parameters as .env file content.

    Args:
        parameters: List of parameter dictionaries

    Returns:
        String containing .env formatted content
    """
    output = []
    for param in parameters:
        # Extract the parameter name after the last slash
        name = param['Name'].split('/')[-1]
        value = param['Value']
        output.append(f"{name}={value}")

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description='Read parameters from AWS Parameter Store and output as .env format')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')
    parser.add_argument('--path', required=True, help='Parameter Store path (e.g., /coursehub/development/)')

    args = parser.parse_args()

    try:
        parameters = get_parameters(args.region, args.path)
        if not parameters:
            print(f"No parameters found at path: {args.path}", file=sys.stderr)
            sys.exit(1)

        print(format_env_output(parameters))

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
