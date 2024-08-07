import boto3
import json

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
BUCKET_PREFIX = "coach_data/"


def lambda_handler(event, context):


    print(event)

    coach_id = event['rawQueryString']
    coach_id = coach_id[len('coach_id='):]

    print("coach_id: " + coach_id)

    response = s3.list_objects_v2(Bucket = BUCKET_NAME,
                                Prefix = BUCKET_PREFIX + coach_id +
                                "/sets" )
    
    meta_response = s3.get_object(Bucket = BUCKET_NAME, Key = BUCKET_PREFIX + coach_id + "/sets/metadata.json")
    file_contents = meta_response["Body"]
    as_string = file_contents.read().decode('utf-8')
    metadata = json.loads(as_string)

    print("Metadata" + json.dumps(metadata))

    sets = []
    for file in response['Contents']:
        if(file['Key'].find("metadata.json") == -1):
            file_string = file['Key']
            start_index = file_string.index("sets/") + len("sets/")
            year = int(file_string[start_index:start_index + 4])
            month_start = start_index + 5
            month_end = file_string.index("-", month_start)
            month = int(file_string[month_start:month_end])
            day_start = month_end + 1
            day_end = file_string.index("-", day_start)
            day = int(file_string[day_start:day_end])
            name = file_string[ day_end + len("-SET-"): len(file_string) - len(".json")]
            set = {
                'year': year,
                'month': month,
                'day': day,
                'name': name,
                'filename': file_string
            }
            sets.append(set)

    print("Sets: " + json.dumps(sets))

    data = {
        'sets': sets,
        'metadata': metadata
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
 
