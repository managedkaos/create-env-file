"""
Unit tests for AWS Parameter Store script
"""

import unittest
from unittest.mock import MagicMock, patch

from script import format_env_output, get_parameters


class TestAWSParameterStoreScript(unittest.TestCase):
    @patch("script.boto3.client")
    def test_get_parameters(self, mock_boto3):
        # Setup mock response
        mock_ssm = MagicMock()
        mock_boto3.return_value = mock_ssm

        # Mock the get_parameters_by_path response
        mock_ssm.get_parameters_by_path.return_value = {
            "Parameters": [
                {"Name": "/test/path/DB_HOST", "Value": "localhost"},
                {"Name": "/test/path/DB_PASSWORD", "Value": "secret123"},
            ]
        }

        # Call the function
        result = get_parameters("us-east-1", "/test/path")

        # Verify the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["Name"], "/test/path/DB_HOST")
        self.assertEqual(result[0]["Value"], "localhost")

        # Verify boto3 was called correctly
        mock_boto3.assert_called_once_with("ssm", region_name="us-east-1")
        mock_ssm.get_parameters_by_path.assert_called_once_with(
            Path="/test/path", Recursive=True, WithDecryption=True
        )

    def test_format_env_output(self):
        # Test data
        parameters = [
            {"Name": "/test/path/DB_HOST", "Value": "localhost"},
            {"Name": "/test/path/DB_PASSWORD", "Value": "secret123"},
        ]

        # Call the function
        result = format_env_output(parameters)

        # Verify the result
        expected_output = "DB_HOST=localhost\nDB_PASSWORD=secret123"
        self.assertEqual(result, expected_output)

    @patch("script.boto3.client")
    def test_get_parameters_pagination(self, mock_boto3):
        # Setup mock response with pagination
        mock_ssm = MagicMock()
        mock_boto3.return_value = mock_ssm

        # First page response
        mock_ssm.get_parameters_by_path.side_effect = [
            {
                "Parameters": [{"Name": "/test/path/DB_HOST", "Value": "localhost"}],
                "NextToken": "token123",
            },
            {"Parameters": [{"Name": "/test/path/DB_PASSWORD", "Value": "secret123"}]},
        ]

        # Call the function
        result = get_parameters("us-east-1", "/test/path")

        # Verify the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["Name"], "/test/path/DB_HOST")
        self.assertEqual(result[1]["Name"], "/test/path/DB_PASSWORD")

        # Verify boto3 was called twice (for pagination)
        self.assertEqual(mock_ssm.get_parameters_by_path.call_count, 2)


if __name__ == "__main__":
    unittest.main()
