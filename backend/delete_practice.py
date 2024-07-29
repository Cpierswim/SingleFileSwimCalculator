import boto3
import json
from urllib.parse import unquote

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "coach_data/"


def lambda_handler(event, context):

    print(event)

    original_filename = event['rawQueryString']
    filename = original_filename[len('filename='):]
    filename = unquote(filename)
    coach_id = filename[len('coach_data/'):]
    coach_id = coach_id[:coach_id.find("/")]
    saved_filename = filename[len('coach_data/' + coach_id + '/practices/'):]

    print("Deleting filename: " + filename)

    response = s3.delete_object(Bucket=BUCKET_NAME, Key=filename)

    print("Accessing metadata file")

    metadata_file_name = BUCKET_PREFIX + coach_id + "/practices/" +  "metadata.json"
    print("metadata_file_name: " + metadata_file_name)

    
    response = s3.get_object(Bucket=BUCKET_NAME, Key=metadata_file_name)
    file_contents = response["Body"]
    as_string = file_contents.read().decode('utf-8')
    metadata = json.loads(as_string)
    key_words = metadata["key_words"]
    key_words = list(key_words.keys()) 

    for word in key_words:
        for practice in metadata['key_words'][word]:
            if(practice == saved_filename):
                metadata['key_words'][word].remove(saved_filename)
                if(len(metadata['key_words'][word]) == 0):
                    del metadata['key_words'][word]
    
    s3.put_object(
        Body = json.dumps(metadata),
        Bucket = BUCKET_NAME,
        Key = metadata_file_name
    )



    return {
        'statusCode': 200
    }


