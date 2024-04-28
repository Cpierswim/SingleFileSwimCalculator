#importing packages 
import json 
import boto3 
from random import randrange
import time

s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"

def deleteFilesPastTTLInFolder(folder):
    deleted = 0
    try:
        if(not folder.endswith("/")):
            folder = folder + "/"
        current_epoch = int(time.time())
        result = s3.list_objects(Bucket = BUCKET_NAME, Prefix=folder)
        for o in result.get('Contents'):
            if o.get('Key') == folder:
                continue
            filename = BUCKET_NAME + "/" + o.get('Key')
            data = s3.get_object(Bucket=BUCKET_NAME, Key=o.get('Key'))
            contents = data['Body'].read()
            contents = contents.decode('utf-8')
            contents = json.loads(contents)

            delete = False
            if not "ttl" in contents.keys():
                delete = True
            else:
                if contents["ttl"] < current_epoch:
                    delete = True
            
            if delete:
                try:
                    print("deleting " + filename)
                    s3.delete_object(Bucket=BUCKET_NAME, Key=o.get('Key'))
                    deleted += 1
                except:
                    pass

        return deleted
    except:
        return deleted



def lambda_handler(event, context):
    deleted = 0
    deleted += deleteFilesPastTTLInFolder("coach_keys")
    deleted += deleteFilesPastTTLInFolder("coachids")
    deleted += deleteFilesPastTTLInFolder("rooms")
    deleted += deleteFilesPastTTLInFolder("connectedIDs")

    return { 
        'statusCode': 202,
        'body': { 
            'message': 'success',
            'deleted': deleted
        }
    }

