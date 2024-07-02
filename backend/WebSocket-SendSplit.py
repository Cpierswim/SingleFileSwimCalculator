import json
import boto3

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://mjim68pp6h.execute-api.us-east-2.amazonaws.com/production/")

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "rooms/"

def lambda_handler(event, context):
    print(event)
    
    print("Getting all connections")
   
    body = json.loads(event['body'])
    room_key = body["roomKey"]

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
    room_data = json.loads(as_string)

    print("Room Data:")
    print(room_data["room_key"])
   
    lane_to_send_to = body["lane_to_send_to"]
    split = body["split"]
    mills_to_display_splits = body["mills_to_display_splits"]
    connected_lanes = room_data["connected_lanes"]

    lane_to_send_to = str(lane_to_send_to)
    print(connected_lanes)

    connection_id = connected_lanes[lane_to_send_to]
    print("Sending message to lane " + lane_to_send_to + " connectionID: " + connection_id)
    message_to_send = {
        "type": "split",
        "split": split,
        "mills_to_display_splits": mills_to_display_splits
    }
    print("Split " + split + " sent")
    print("Sending message: " + json.dumps(message_to_send))
    client.post_to_connection(
        Data=json.dumps(message_to_send).encode('utf-8'),
        ConnectionId=connection_id
    )
   
   
    return { "statusCode": 200  }