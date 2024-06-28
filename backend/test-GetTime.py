import json
import time
import boto3

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://mjim68pp6h.execute-api.us-east-2.amazonaws.com/production/")


def lambda_handler(event, context):

    data = {
        "timestamp": int(time.time() * 1000),
        "type": "timestamp",
        "initial_time": json.loads(event['body'])["initial_time"]
    }

    
    client.post_to_connection(ConnectionId=event["requestContext"]["connectionId"], Data=json.dumps(data).encode('utf-8'))

    return {
        'statusCode': 200
    }