import os
import sys
import json
import boto3
import pytest
from pathlib import Path
from moto import mock_dynamodb2

# Set environment variables before imports
os.environ['AWS_REGION'] = 'us-east-1'
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# Now import your Lambda handler
from src.app import lambda_handler

@pytest.fixture
def dynamodb_mock():
    with mock_dynamodb2():
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        # Set up the mocked table here if your Lambda assumes it already exists
        table_name = "Visits"
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "ID", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "ID", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        )
        yield dynamodb

def test_lambda_handler_increments_counter(dynamodb_mock):
    response = lambda_handler({}, None)
    assert response['statusCode'] == 200
    assert json.loads(response['body'])['visit_count'] == 1

def test_lambda_handler_creates_counter_if_missing(dynamodb_mock):
    table = dynamodb_mock.Table("Visits")
    table.delete_item(Key={'ID': '1'})
    response = lambda_handler({}, None)
    assert response['statusCode'] == 200
