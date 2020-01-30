import json
import boto3
import os


def post(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    
    linksTable = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    linksTable.put_item(Item=json.loads(event['body']))

    response = {
        "statusCode": 201
    }

    return response