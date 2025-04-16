import os
import sys
from pathlib import Path
import boto3
import pytest
from moto import mock_dynamodb2

# Set environment variables before imports
os.environ['AWS_REGION'] = 'us-east-1'

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# Now import your Lambda handler
from src.app import lambda_handler

@pytest.fixture
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.create_table(
            TableName='resume-apptbl',
            KeySchema=[{'AttributeName': 'ID', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'ID', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        table.put_item(Item={'ID': '1', 'counter': 0})
        yield table

def test_lambda_handler_increments_counter(dynamodb_mock):
    response = lambda_handler({}, None)
    assert response['statusCode'] == 200
    assert json.loads(response['body'])['visit_count'] == 1

def test_lambda_handler_creates_counter_if_missing(dynamodb_mock):
    dynamodb_mock.delete_item(Key={'ID': '1'})
    response = lambda_handler({}, None)
    assert json.loads(response['body'])['visit_count'] == 1