import boto3
import os
import json
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('Visits')

def lambda_handler(event, context):
    try:
        response = table.update_item(
            Key={'ID': '1'},
            UpdateExpression='SET #ctr = if_not_exists(#ctr, :start) + :inc',
            ExpressionAttributeNames={'#ctr': 'counter'},
            ExpressionAttributeValues={':inc': 1, ':start': 0},
            ReturnValues='UPDATED_NEW'
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'visit_count': int(response['Attributes']['counter'])})
        }
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
