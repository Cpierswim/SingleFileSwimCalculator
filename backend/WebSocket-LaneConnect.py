import json
import boto3

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://mjim68pp6h.execute-api.us-east-2.amazonaws.com/production/")

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "rooms/"
BUCKET_CONNECTION_PREFIX = "connectedIDs/"
        
        

def lambda_handler(event, context):

    print("Attempting to connect Lane to Coach")
    

    
    print("Event:")
    print(event)
    print("Context:")
    print(context)
    
    connectionID = event["requestContext"]["connectionId"]
    message_body = json.loads(event["body"])
    roomKey = message_body["roomKey"].upper()
    LaneNumber = message_body["LaneNumber"]

    key_file_name = BUCKET_PREFIX + roomKey + ".json"

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

    print("Old Data:")
    print(data)

    coachID = data["coachID"]
    connected_lanes = data["connected_lanes"]

    if LaneNumber in connected_lanes.keys():
        print ("Attempting to connect to lane already in connected")
        message_data = {
            "type": "error",
            "message": "Lane already connected"
        }

        client.post_to_connection(ConnectionId=connectionID, Data=json.dumps(message_data).encode('utf-8'))

        return {
            'statusCode': 200,
        }
    
    connected_lanes[LaneNumber] = connectionID
    data["connected_lanes"] = connected_lanes

    print("New Data:")
    print(data)

    print("Writing new data: ")
    print(data)

    s3.put_object(
            Body = json.dumps(data),
            Bucket = BUCKET_NAME,
            Key = key_file_name
        )
    
    print("File written sucessfully")

    print("Sending message to coach with ID: " + coachID)

    message_data = {
        "type": "LaneConnect",
        "laneNumber": LaneNumber
    }

    
    client.post_to_connection(ConnectionId=coachID, Data=json.dumps(message_data).encode('utf-8'))  
    print("Sent data to coach")
    swimmmer_message_data = {
        "type": "LaneConnect",
        "laneNumber": LaneNumber
    }
    client.post_to_connection(ConnectionId=connectionID, Data=json.dumps(swimmmer_message_data).encode('utf-8'))
    print("Sent data to swimmer")

    print("Updting swimmer connection info to include room")

    connection_file_name = BUCKET_CONNECTION_PREFIX + connectionID + ".json"
    print("Accessing file: " + connection_file_name)

    response = ""
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=connection_file_name)
    except:
        print("Error accessing file")
        return {
            'statusCode': 404,
            'message': "connection not found"
        }
    print("Connection Found: " + connectionID)

    file_contents = response["Body"]
    file_as_string = file_contents.read().decode('utf-8')
    data = json.loads(file_as_string)

    print("Old Data:")
    print(data)

    data["room"] = roomKey

    print("New Data:")
    print(data)

    print("Writing new data: ")

    s3.put_object(
            Body = json.dumps(data),
            Bucket = BUCKET_NAME,
            Key = connection_file_name
        )
    
    print("File written sucessfully")


    return {
        'statusCode': 200
    }
