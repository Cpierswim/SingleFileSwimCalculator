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


temp = {
  "version": "2.0",
  "routeKey": "$default",
  "rawPath": "/filename=coach_data%2FCpierswim%2Fpractices%2F2024-7-25-PRACTICE-1-test%20bronze.json",
  "rawQueryString": "",
  "headers": {
    "x-amzn-tls-cipher-suite": "TLS_AES_128_GCM_SHA256",
    "x-amzn-tls-version": "TLSv1.3",
    "x-amzn-trace-id": "Root=1-66a3020e-12fe1b0645691f351df52210",
    "x-forwarded-proto": "https",
    "postman-token": "b58149fe-a3be-4211-a9a6-a81c7a83c5aa",
    "host": "lufypj7qre3hbvkvasijiv7rhy0tvrtr.lambda-url.us-east-2.on.aws",
    "x-forwarded-port": "443",
    "x-forwarded-for": "76.205.200.33",
    "accept-encoding": "gzip, deflate, br",
    "accept": "*/*",
    "user-agent": "PostmanRuntime/7.37.3"
  },
  "requestContext": {
    "accountId": "anonymous",
    "apiId": "lufypj7qre3hbvkvasijiv7rhy0tvrtr",
    "domainName": "lufypj7qre3hbvkvasijiv7rhy0tvrtr.lambda-url.us-east-2.on.aws",
    "domainPrefix": "lufypj7qre3hbvkvasijiv7rhy0tvrtr",
    "http": {
      "method": "GET",
      "path": "/filename=coach_data/Cpierswim/practices/2024-7-25-PRACTICE-1-test bronze.json",
      "protocol": "HTTP/1.1",
      "sourceIp": "76.205.200.33",
      "userAgent": "PostmanRuntime/7.37.3"
    },
    "requestId": "8325a27e-b5d0-4b02-83dd-b07218b813db",
    "routeKey": "$default",
    "stage": "$default",
    "time": "26/Jul/2024:01:55:26 +0000",
    "timeEpoch": 1721958926045
  },
  "isBase64Encoded": False
}

lambda_handler(temp, None)