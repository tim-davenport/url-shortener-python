import json
import boto3
import os
import validators
import string
import random

def post(event, context):
    
    body = event['body']

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

    links_table.put_item(Item={"code":"short_code", "url":url})

    response = {
        "statusCode": 201,
        "headers": {
            "Location": ""
        }
    }

    return response

def get(event, context):
    response = {
        "statusCode": 302,
        "headers": {
            "Location": ""
        }
    }

    return response