from moto import mock_aws
import boto3
import pytest

TABLE_NAME = "Visits"

@pytest.fixture
def dynamodb_mock():
    with mock_aws():
        # Setup mock table
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "ID", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "ID", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        yield dynamodb

# ✅ Add this test function:
def test_table_exists(dynamodb_mock):
    table = dynamodb_mock.Table(TABLE_NAME)
    table.load()  # Will raise if table does not exist
    assert table.table_status == "ACTIVE"
