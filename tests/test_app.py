import os
import sys
import json
import boto3
import pytest
from moto import mock_dynamodb
from pathlib import Path

# Set region before anything else
os.environ["AWS_DEFAULT_REGION"] = "us-west-1"

# Add project root to path for importing src
sys.path.append(str(Path(__file__).parent.parent))

# Import your Lambda function
from src.app import lambda_handler

@pytest.fixture
def dynamodb_mock():
    with mock_dynamodb():
        # Set up mock DynamoDB
        dynamodb = boto3.resource('dynamodb')

        # Create the test table (adjust name/key as needed)
        table = dynamodb.create_table(
            TableName='visit-counter',
            KeySchema=[
                {'AttributeName': 'ID', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'ID', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        yield dynamodb

def test_lambda_handler_increments_counter(dynamodb_mock):
    response = lambda_handler({}, None)
    assert response['statusCode'] == 200
    assert json.loads(response['body'])['visit_count'] == 1

def test_lambda_handler_creates_counter_if_missing(dynamodb_mock):
    # Ensure counter is missing
    table = dynamodb_mock.Table('visit-counter')
    table.delete_item(Key={'ID': '1'})

    # Call handler
    response = lambda_handler({}, None)
    assert response['statusCode'] == 200
    assert json.loads(response['body'])['visit_count'] == 1
