import boto3
import os
import json
from boto3.dynamodb.conditions import Attr

# Set up DynamoDB resource and table
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Visits')

def lambda_handler(event, context):
    try:
        # Update the visitor count
        response = table.update_item(
            Key={'ID': '1'},  # This is the partition key for the DynamoDB table
            UpdateExpression='SET #ctr = if_not_exists(#ctr, :start) + :inc',
            ExpressionAttributeNames={'#ctr': 'counter'},
            ExpressionAttributeValues={':inc': 1, ':start': 0},
            ReturnValues='UPDATED_NEW'
        )
        
        # Return updated visitor count
        return {
            'statusCode': 200,
            'body': json.dumps({'visit_count': int(response['Attributes']['counter'])})
        }
    except Exception as e:
        # Return error if something goes wrong
        print(f"Error: {str(e)}")  # Log the error for debugging
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
