import json
import boto3
import time

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "connectedIDs/"

def lambda_handler(event, context):
    print(event)
    print("****")
    print(context)

    print("New Connection Created - adding to stored Connection IDs")

    connectionId = event["requestContext"]["connectionId"]

    filename = BUCKET_PREFIX + connectionId + ".json"

    ttl = int(time.time()) + (4 * 60 * 60)

    data = {
        "connectionId": connectionId,
        "type": "unknown",
        "ttl": ttl
    }

    s3.put_object(
            Body = json.dumps(data),
            Bucket = BUCKET_NAME,
            Key = filename
        )

    
    
    return {'statusCode': 200}