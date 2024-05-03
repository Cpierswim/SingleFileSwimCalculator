import json
import boto3

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://mjim68pp6h.execute-api.us-east-2.amazonaws.com/production/")

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "rooms/"

def lambda_handler(event, context):
    print(event)
    print(context)

    print("Getting all connections")

    body = json.loads(event['body'])
    room_key = body["roomKey"]
    minutes =  body["minutes"]
    seconds = body["seconds"]
    time_stamp = body["time_stamp"]

    key_file_name = BUCKET_PREFIX + room_key + ".json"

    print("Accessing file: " + key_file_name)
    
    response = ""

    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key_file_name)
    except:
        return {
            'statusCode': 404,
            'message': "room not found"
        }
    
    print("Room Key Found:")
    file_contents = response["Body"]
    as_string = file_contents.read().decode('utf-8')
    data = json.loads(as_string)

    print("Room Data:")
    print(data)

    coachID = data["coachID"]
    connected_lanes = data["connected_lanes"]

    message_data = {
            "type": "ping",
            "minutes": minutes,
            "seconds": seconds,
            "time_stamp": time_stamp,
            "roomKey": room_key
        }

    for LaneNumber in connected_lanes.keys():
        pass

    print ("Attempting to send to coach: " + coachID)
    client.post_to_connection(ConnectionId=coachID, Data=json.dumps(message_data).encode('utf-8'))

    print("Message sent")

    return {
        'statusCode': 200,
    }