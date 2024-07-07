import json
import boto3

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://mjim68pp6h.execute-api.us-east-2.amazonaws.com/production/")

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "coach_videos/"
    
        

def lambda_handler(event, context):

    print("Starting to get coach videos")
    print("Event:")
    print(event)
    print("Context:")
    print(context)

    connectionID = event["requestContext"]["connectionId"]
    message_body = json.loads(event["body"])
    coachID = message_body["coachID"]
    print("Coach ID: " + coachID)
    file_name = BUCKET_PREFIX + coachID + ".json"

    
    
    print("Accessing file: " + file_name)

    response = ""
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)
    except:
        print("No coach video file found")

        message_data = {
            "type": "coachVideoList",
            "coachVideos": {}
        }

        client.post_to_connection(ConnectionId=connectionID, Data=json.dumps(message_data).encode('utf-8'))
        return {
        'statusCode': 200
        }
    
    print("Coach Video File Found:")
    file_contents = response["Body"]
    as_string = file_contents.read().decode('utf-8')
    data = json.loads(as_string)

    message_data = {
        "type": "coachVideoList",
        "coachVideos": data
    }

    print("Sending coach videos to client")
    print(message_data)

    client.post_to_connection(ConnectionId=connectionID, Data=json.dumps(message_data).encode('utf-8'))

    print("Coach Videos Sent")

    return {
        'statusCode': 200
    }
