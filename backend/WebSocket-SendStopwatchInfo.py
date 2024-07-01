import json
import boto3

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://mjim68pp6h.execute-api.us-east-2.amazonaws.com/production/")

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "rooms/"

def lambda_handler(event, context):
    print(str(event))
    
    print("Getting all connections")
   
    body = json.loads(event['body'])
    room_key = body["roomKey"]

    key_file_name = BUCKET_PREFIX + room_key + ".json"

    print("Accessing file: " + str(key_file_name))
    
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
    room_data = json.loads(as_string)

    print("Room Key: "  + str(room_data["room_key"]))

    connected_lanes = room_data["connected_lanes"]
    print("Connected Lanes:\n" + str(connected_lanes))
   
    lane_number = str(body["lane_number"])
    connection_id = connected_lanes[lane_number]

    print("Sending message to lane " + str(lane_number) + " connectionID: " + str(connection_id))
    message_to_send = {
        "type": "stopwatchinfo",
        "time": body["time"]
    }
    print("Sending message:\n" + str(message_to_send))
    client.post_to_connection(
        Data=json.dumps(message_to_send).encode('utf-8'),
        ConnectionId=connection_id
    )   
   
    return { "statusCode": 200  }