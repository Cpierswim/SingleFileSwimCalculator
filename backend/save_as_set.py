import json
import boto3
import datetime

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "coach_data/"

def lambda_handler(event, context):
    print("Event:")
    print(event)
    print("Context:")
    print(context)

    body = json.loads(event['body'])
    print("Body:")
    print(body)
    set = body['set']
    print("Set")
    print(set)
    dumped = json.dumps(set)

    print("Saving set...")

    filename = body['filename']
    print("Filename: " + filename)

    coach_id = body['coach_id']
    print("coach_id: " + coach_id)

    full_path = BUCKET_PREFIX + coach_id + "/sets/" + filename
    print("Full path:" + full_path)

    data = {
        'set': set, 
        'name': body['name'],
        'date': body['date'],
        'key_words': body['key_words'],
        'description': body['description']
    }


    s3.put_object(
            Body = json.dumps(data),
            Bucket = BUCKET_NAME,
            Key = full_path
        )
    

    print("Accessing metadata file")

    metadata_file_name = BUCKET_PREFIX + coach_id + "/sets/" +  "metadata.json"
    print("metadata_file_name: " + metadata_file_name)

    metadata = {}

    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=metadata_file_name)
        file_contents = response["Body"]
        as_string = file_contents.read().decode('utf-8')
        metadata = json.loads(as_string)
    except:
        pass

    if ("key_words" not in list(metadata.keys())):
        metadata["key_words"] = {}

    print("Metadata: " + json.dumps(metadata))

    key_words = body['key_words']
    key_words = key_words.split(",")

    previous_key_words = list( metadata.keys())

    for word in key_words:
        word = word.strip()
        found = False
        for key_word in previous_key_words:
            if(word.upper() == key_word.upper()):
                found = True
        if(not found):
            metadata['key_words'][word] = []

        metadata['key_words'][word].append(filename)

    s3.put_object(
        Body = json.dumps(metadata),
        Bucket = BUCKET_NAME,
        Key = metadata_file_name
    )
            

    return {
            'statusCode': 200,
        }
