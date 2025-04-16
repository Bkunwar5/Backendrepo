
import os
import json
import boto3
from moto import mock_dynamodb
import pytest

# Mock environment variables
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

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
        # Initialize with test data
        table.put_item(Item={'ID': '1', 'counter': 0})
        yield table

def test_lambda_handler_increments_counter(dynamodb_mock):
    from src.app import lambda_handler
    
    # First invocation
    response1 = lambda_handler({}, None)
    data1 = json.loads(response1['body'])
    assert response1['statusCode'] == 200
    assert data1['visit_count'] == 1
    
    # Second invocation
    response2 = lambda_handler({}, None)
    data2 = json.loads(response2['body'])
    assert data2['visit_count'] == 2

def test_lambda_handler_creates_counter_if_missing(dynamodb_mock):
    from src.app import lambda_handler
    
    # Clear the table
    dynamodb_mock.delete_item(Key={'ID': '1'})
    
    # First invocation on empty table
    response = lambda_handler({}, None)
    data = json.loads(response['body'])
    assert data['visit_count'] == 1