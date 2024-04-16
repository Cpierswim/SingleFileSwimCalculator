#importing packages 
import json 
import boto3 
from random import randrange


s3 = boto3.client('s3')
BUCKET_NAME = "swimcalculator"
response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='coach_keys/')
UsedKeys = []
for file in response['Contents'] :
    if(file['Key'] == 'coach_keys/'):
        continue
    else:
        name = file['Key'].split('/')[-1]
        key = name.split('.')[0]
        UsedKeys.append(key)

UsedKeys.append("AAA")


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
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
               'Y', 'Z']

for i in range(len(bad_words_list)):
    bad_words_list[i] = bad_words_list[i].upper()


def get_random_code():

    code = letters[randrange(0, 25)] + letters[randrange(25)] + letters[randrange(25)]
    
    if(code in bad_words_list):
        print("Bad word found: " + code + ". Trying again.")
        return get_random_code()
    else:

        if code in UsedKeys:
            code = get_random_code()

        return code
            

def lambda_handler2(event, context):
    if not 'id' in event.keys():
        return {
            'statusCode': 401,
            'body': {
                'message': "no id provided"
            }
        }
    id = event['id']

    filename = "coachids/" + id + ".json"
    try:
        data = s3.get_object(Bucket='swimcalculator', Key=filename)
        #if we find the file, the id is already in use
        return {
            'statusCode': 401,
            'message': "That ID is already in use"
        }
    except:
        # this is actually where we want to be

        coach_key = get_random_code()

        key_file_name = "coach_keys/" + coach_key + ".json"

        data = {
            "id": id,
            "key": coach_key
        }

        s3.put_object(
            Body = json.dumps(data),
            Bucket = BUCKET_NAME,
            Key = filename
        )

        s3.put_object(
            Body = json.dumps(data),
            Bucket = BUCKET_NAME,
            Key = key_file_name
        )

        return {
                'statusCode': 201,
                'body': data
            }   