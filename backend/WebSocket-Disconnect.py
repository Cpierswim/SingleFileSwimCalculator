import json
import boto3

BUCKET_NAME = "swimcalculator"
BUCKET_CONNECTION_PREFIX = "connectedIDs/"
BUCKET_ROOM_PREFIX = "rooms/"

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://mjim68pp6h.execute-api.us-east-2.amazonaws.com/production/")

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("User disconnected")
    print("Event:")
    print(event)
    print("Context:")
    print(context)

    connectionId= event["requestContext"]["connectionId"]

    print("Getting connection data for " + connectionId)

    connection_file_name = BUCKET_CONNECTION_PREFIX + connectionId + ".json"
    print("Accessing file: " +  connection_file_name)

    response = ""  
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=connection_file_name)
    except:
        print("Conneciton file not found")
        return {
            'statusCode': 404,
            'message': "connection not found"
        }
    print("Connection found: " + connectionId)

    file_contents = response["Body"]
    file_as_string = file_contents.read().decode('utf-8')
    data = json.loads(file_as_string)

    print("Connection Data:")
    print(data)

    print("Deleting connection data")

    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=connection_file_name
    )

    print("Connection data deleted sucessfully")


    if(data["type"] == "coach"):
        print("Connection was a coach")
        if("room" in data.keys()):
            print("Coach was in a room. Attempting to remove from room")
            room_file_name = BUCKET_ROOM_PREFIX + data["room"] + ".json"
            print("Accessing file: " +  room_file_name)
            response = ""
            try:
                response = s3.get_object(Bucket=BUCKET_NAME, Key=room_file_name)
                print("Room file found")
            except:
                print("Room file not found")
                return {
                    'statusCode': 200
                }
            
            file_contents = response["Body"]
            file_as_string = file_contents.read().decode('utf-8')
            data = json.loads(file_as_string)

            print("Room Data:")
            print(data)

            print("Removing coach from room")
            data["coachID"] = ""

            print("Writing new data")
            print(data)

            s3.put_object(
                Body = json.dumps(data),
                Bucket = BUCKET_NAME,
                Key = room_file_name
            )

            print("Room data updated sucessfully")
    elif (data["type"] == "swimmer"):
        print("Connection was a swimmer")
        if("room" in data.keys()):
            print("Attempting to remove swimmer from room")
            room_file_name = BUCKET_ROOM_PREFIX + data["room"] + ".json"
            print("Accessing file: " +  room_file_name)
            response = ""
            try:
                response = s3.get_object(Bucket=BUCKET_NAME, Key=room_file_name)
                print("Room file found")
            except:
                print("Room file not found")
                return {
                    'statusCode': 200
                }
            
            file_contents = response["Body"]
            file_as_string = file_contents.read().decode('utf-8')
            data = json.loads(file_as_string)

            print("Old Room Data:")
            print(data)

            print("Removing Lane from room")
            lane_disconnected = -1
            for lane, connection_ID in data["connected_lanes"].items():
                if(connection_ID == connectionId):
                    print("Connection found at lane "+ lane)
                    del data["connected_lanes"][lane]
                    lane_disconnected = lane
                    print("Lane " + lane + " diconnected")
                    break

            print("New Room Data:")
            print(data)

            s3.put_object(
                Body = json.dumps(data),
                Bucket = BUCKET_NAME,
                Key = room_file_name
            )

            print("Room data updated sucessfully")

            if(lane_disconnected == -1):
                print("Lane not found")
                return {
                    'statusCode': 200
                }
            print("Sending message to coach with ID: " + data["coachID"])

            message_data = {
                "type": "LaneDisconnect",
                "laneNumber": lane_disconnected
            }

            print("Message Data:")
            print(message_data)
            client.post_to_connection(ConnectionId=data["coachID"], Data=json.dumps(message_data).encode('utf-8'))

            print("Message sent")


    return {
        'statusCode': 200
    }
