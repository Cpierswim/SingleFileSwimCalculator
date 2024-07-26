import boto3
import json

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "coach_data/"


def lambda_handler(event, context):


    print(event)

    coach_id = event['rawQueryString']
    coach_id = coach_id[len('coach_id='):]

    print("coach_id: " + coach_id)

    response = s3.list_objects_v2(Bucket = BUCKET_NAME,
                                Prefix = BUCKET_PREFIX + "Cpierswim/practices" )
    
    meta_response = s3.get_object(Bucket = BUCKET_NAME, Key = BUCKET_PREFIX + "Cpierswim/practices/metadata.json")
    file_contents = meta_response["Body"]
    as_string = file_contents.read().decode('utf-8')
    metadata = json.loads(as_string)

    print("Metadata" + json.dumps(metadata))

    practices = []
    for file in response['Contents']:
        if(file['Key'].find("metadata.json") == -1):
            file_string = file['Key']
            start_index = file_string.index("practices/") + len("practices/")
            year = int(file_string[start_index:start_index + 4])
            month_start = start_index + 5
            month_end = file_string.index("-", month_start)
            month = int(file_string[month_start:month_end])
            day_start = month_end + 1
            day_end = file_string.index("-", day_start)
            day = int(file_string[day_start:day_end])
            practice_of_the_day_start = day_end + len("-PRACTICE-")
            practice_of_the_day_end = file_string.index("-", practice_of_the_day_start)
            practice_of_the_day = int(file_string[practice_of_the_day_start:practice_of_the_day_end])
            group = file_string[practice_of_the_day_end + 1: -5]
            practice = {
                'year': year,
                'month': month,
                'day': day,
                'practice_of_the_day': practice_of_the_day,
                'group': group,
                'filename': file_string
            }
            practices.append(practice)

    print("Practices: " + json.dumps(practices))

    data = {
        'practices': practices,
        'metadata': metadata
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
 

event = {
  "version": "2.0",
  "routeKey": "$default",
  "rawPath": "/",
  "rawQueryString": "coach_id=Cpierswim",
  "headers": {
    "sec-fetch-mode": "cors",
    "x-amzn-tls-version": "TLSv1.3",
    "sec-fetch-site": "cross-site",
    "x-forwarded-proto": "https",
    "accept-language": "en-US,en;q=0.9,fy;q=0.8",
    "origin": "null",
    "x-forwarded-port": "443",
    "x-forwarded-for": "2600:1700:d70:4e60:bcd2:6037:a6ed:a7e5",
    "accept": "*/*",
    "authorization": "Bearer your-token",
    "coach_id": "Cpierswim",
    "x-amzn-tls-cipher-suite": "TLS_AES_128_GCM_SHA256",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "x-amzn-trace-id": "Root=1-66a2fd8b-79ac92d6068da0af654a642c",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "host": "c6a7fgweplcxu3yjgx5gkklxce0nopqg.lambda-url.us-east-2.on.aws",
    "content-type": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "sec-fetch-dest": "empty"
  },
  "queryStringParameters": {
    "coach_id": "Cpierswim"
  },
  "requestContext": {
    "accountId": "anonymous",
    "apiId": "c6a7fgweplcxu3yjgx5gkklxce0nopqg",
    "domainName": "c6a7fgweplcxu3yjgx5gkklxce0nopqg.lambda-url.us-east-2.on.aws",
    "domainPrefix": "c6a7fgweplcxu3yjgx5gkklxce0nopqg",
    "http": {
      "method": "GET",
      "path": "/",
      "protocol": "HTTP/1.1",
      "sourceIp": "2600:1700:d70:4e60:bcd2:6037:a6ed:a7e5",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    },
    "requestId": "11511034-e447-453f-8cda-feaf7d3149a8",
    "routeKey": "$default",
    "stage": "$default",
    "time": "26/Jul/2024:01:36:11 +0000",
    "timeEpoch": 1721957771118
  },
  "isBase64Encoded": False
}

lambda_handler(event, None)