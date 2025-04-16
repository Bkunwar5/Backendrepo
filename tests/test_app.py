import boto3
import pytest
from moto import mock_dynamodb
from src.app import lambda_handler

TABLE_NAME = "Visits"

@pytest.fixture
def dynamodb_mock():
    with mock_dynamodb():
        # Create DynamoDB resource and table
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "ID", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "ID", "AttributeType": "S"}
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )

        # Wait for table to become active
        table = dynamodb.Table(TABLE_NAME)
        table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)

        yield dynamodb  # this is passed into the tests

def test_lambda_handler_increments_counter(dynamodb_mock):
    response = lambda_handler({}, None)
    assert "visits" in response

def test_lambda_handler_creates_counter_if_missing(dynamodb_mock):
    table = dynamodb_mock.Table(TABLE_NAME)
    table.delete_item(Key={"ID": "1"})  # clear any preexisting data

    response = lambda_handler({}, None)
    assert "visits" in response
