import json
import boto3
import os
import validators
import string
import random

def post(event, context):
    
    body = json.loads(event['body'])

    if 'url' not in body:
        return {
            "statusCode": 400,
            "body": {
                "message": "Please supply a URL in the body of the request"
            }
        }
    else:
        url = body['url']

    if not validators.url(url):
        return {
            "statusCode": 400,
            "body": {
                "message": "Please supply a valid URL"
            }
        }

    short_code = ''.join(random.choice(string.ascii_lowercase) for i in range(6))

    dynamo_db = boto3.resource('dynamodb')

    links_table = dynamo_db.Table(os.environ['DYNAMODB_TABLE'])

    links_table.put_item(Item={"code":short_code, "url":url})

    response = {
        "statusCode": 201,
        "headers": {
            "Location": f'https://{os.environ["APP_URL"]}/{short_code}'
        }
    }

    return response

def get(event, context):

    query_string = event['queryStringParameters']

    if 'code' not in query_string:
        return {
            "statusCode": 400,
            "body": {
                "message": "Please supply a short_code"
            }
        }
    else:
        short_code = query_string['code']

    dynamo_db = boto3.resource('dynamodb')

    links_table = dynamo_db.Table(os.environ['DYNAMODB_TABLE'])

    result = links_table.get_item(
        Key={
            'code': short_code
        }
    )

    item = result['Item']

    response = {
        "statusCode": 302,
        "headers": {
            "Location": item['url']
        }
    }

    return response