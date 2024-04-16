#importing packages 
import json 
import boto3 
from random import randrange
import time

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"

def lambda_handler(event, context):
    try:
        if event is None:
            return{
                'statusCode': 400,
                'message': "no key provided"
            }
        if "key" not in event:
            return{
                'statusCode': 400,
                'message': "no key provided"
            }

        key = event["key"]
        key_file_name = "coach_keys/" + key + ".json"

        

        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=key_file_name)
        except:
            return{
                'statusCode': 404,
                'message': "id not found"
            }
        body = response["Body"]
        as_string = body.read().decode('utf-8')
        as_json = json.loads(as_string)
        id = as_json["id"]

        return{
            'statusCode': 200, 
            'body': { "id": id }
        }
    except:
        return{
            'statusCode': 500, 
            'message': "code error"
        }
