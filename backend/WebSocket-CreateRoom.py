import json
import boto3
from random import randrange
import time

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://mjim68pp6h.execute-api.us-east-2.amazonaws.com/production/")

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "rooms/"
BUCKET_CONNETION_ID_PREFIX = "connectedIDs/"
response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=BUCKET_PREFIX)
UsedKeys = []
for file in response['Contents'] :
    if(file['Key'] == BUCKET_PREFIX):
        continue
    else:
        name = file['Key'].split('/')[-1]
        key = name.split('.')[0]
        UsedKeys.append(key)

bad_words_list = ["ass", "fuc", "fuk", "fuq", "fux", "fck", "coc", "cok", "coq", "kox", 
"koc", "kok", "koq", "cac", "cak", "caq", "kac", "kak", "kaq", "dic", "dik", "diq", "dix", 
"dck", "pns", "psy", "fag", "fgt", "ngr", "nig", "cnt", "knt", "sht", "dsh", "twt", "bch", 
"cum", "clt", "kum", "klt", "suc", "suk", "suq", "sck", "lic", "lik", "liq", "lck", "jiz", 
"jzz", "gay", "gey", "gei", "gai", "vag", "vgn", "sjv", "fap", "prn", "lol", "jew", "joo", 
"gvr", "pus", "pis", "pss", "snm", "tit", "fku", "fcu", "fqu", "hor", "slt", "jap", "wop", 
"kik", "kyk", "kyc", "kyq", "dyk", "dyq", "dyc", "kkk", "jyz", "prk", "prc", "prq", "mic", 
"mik", "miq", "myc", "myk", "myq", "guc", "guk", "guq", "giz", "gzz", "sex", "sxx", "sxi", 
"sxe", "sxy", "xxx", "wac", "wak", "waq", "wck", "pot", "thc", "vaj", "vjn", "nut", "std", 
"lsd", "poo", "azn", "pcp", "dmn", "orl", "anl", "ans", "muf", "mff", "phk", "phc", "phq", 
"xtc", "tok", "toc", "toq", "mlf", "rac", "rak", "raq", "rck", "sac", "sak", "saq", "pms", 
"nad", "ndz", "nds", "wtf", "sol", "sob", "fob", "sfu"]
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
               'M', 'N',  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
               'Y', 'Z']
               

def get_random_code():
    
    number_of_letters = len(letters)

    code = letters[randrange(0, number_of_letters)] + letters[randrange(number_of_letters)] + letters[randrange(number_of_letters)]
    
    if(code.lower() in bad_words_list):
        print("Bad word found: " + code + ". Trying again.")
        return get_random_code()
    else:

        if code in UsedKeys:
            code = get_random_code()

        return code
        
        

def lambda_handler(event, context):

    print("Starting to create room")
    
    room_key = get_random_code()
    
    print("Event:")
    print(event)
    print("Context:")
    print(context)
    
    coachID = event["requestContext"]["connectionId"]
    
    print("Creating room " + room_key + " for coachID " + coachID)
    
    filename = BUCKET_PREFIX + room_key + ".json"
    ttl = int(time.time()) + (4 * 60 * 60)

    data = {
            "coachID": coachID,
            "room_key": room_key,
            "ttl": ttl,
            "connected_lanes": {}
        }
        
    print("Data: ")
    print(data)
    
    data_dumps = json.dumps(data)
    
    s3.put_object(
            Body = data_dumps,
            Bucket = BUCKET_NAME,
            Key = filename
        )
    
    return_message = {
        "type": "RoomCreated",
        "data": data
    }
        
    response = client.post_to_connection(ConnectionId=coachID, Data=json.dumps(return_message).encode('utf-8'))

    print("Room data sent to requester")

    print("Updating Connection file")

    connection_file_name = BUCKET_CONNETION_ID_PREFIX + coachID + ".json"

    print("Accessing file: " + connection_file_name)
    response = ""

    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=connection_file_name)
    except:
        print("Error accessing file")
        return {
            'statusCode': 404,
            'message': 'conneciton not found'
        }
   
    print("Connection found: " + coachID)

    file_contents = response["Body"]
    file_as_string = file_contents.read().decode('utf-8')
    data = json.loads(file_as_string)

    print("Old Data:")
    print(data)

    data["room"] = room_key

    print("New Data:")
    print(data)

    print("Writing new data")

    s3.put_object(
        Body = json.dumps(data),
        Bucket = BUCKET_NAME,
        Key = connection_file_name
    )

    print("File written successfully")

    return {
        'statusCode': 200
    }
