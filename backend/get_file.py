import boto3
import json
from urllib.parse import unquote

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"


def lambda_handler(event, context):
    print(event)

    filename = event['rawPath']
    filename = filename[len('filename='):]
    filename = unquote(filename)

    print("Getting filename: " + filename)

    response = s3.get_object(Bucket=BUCKET_NAME, Key=filename)

    file_contents = response["Body"]
    as_string = file_contents.read().decode('utf-8')
    practice = json.loads(as_string)

    return {
        'statusCode': 200,
        'body': json.dumps(practice)
    }

