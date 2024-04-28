import json
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "connectedIDs/"

def lambda_handler(event, context):

    print("Attempting to set connection type")
    print("Event:")
    print(event)
    print("Context:")
    print(context)
    
    connectionID = event["requestContext"]["connectionId"]
    message_body = json.loads(event["body"])
    connection_type = message_body["type"]

    connection_file_name = BUCKET_PREFIX + connectionID + ".json"

    print("Accessing file: " +  connection_file_name)

    response = ""

    try: 
        response = s3.get_object(Bucket=BUCKET_NAME, Key=connection_file_name)
    except:
        return {
            'statusCode': 404,
            'message': "connection not found"
        }
    
    print("Conneciton Found: " + connectionID)

    file_contents = response["Body"]
    file_as_string = file_contents.read().decode('utf-8')
    data = json.loads(file_as_string)

    print("Old Data:")
    print(data)

    data["type"] = connection_type

    print("New Data:")
    print(data)

    print("Writing new data: ")

    s3.put_object(
            Body = json.dumps(data),
            Bucket = BUCKET_NAME,
            Key = connection_file_name
        )
    
    print("File written successfully")

    return {
        'statusCode': 200,
    }
