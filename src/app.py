
import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('resume-apptbl')

def lambda_handler(event, context):
    # Use an atomic update operation to increment the counter
    response = table.update_item(
        Key={'ID': '1'},
        UpdateExpression="SET #ctr = if_not_exists(#ctr, :start) + :inc",
        ExpressionAttributeNames={'#ctr': 'counter'},  # Alias for reserved keyword
        ExpressionAttributeValues={
            ':start': Decimal(0),  # Default value if 'counter' does not exist
            ':inc': Decimal(1)     # Increment by 1
        },
        ReturnValues="UPDATED_NEW"
    )

    visit_count = int(response['Attributes']['counter'])  # Convert Decimal to int

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps({'visit_count': visit_count})  # Now JSON serializable
    }