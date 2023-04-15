import json
import boto3
import subprocess
import shlex
import os

def response_proxy(data):
	response = {}
	response["isBase64Encoded"] = False
	response["statusCode"] = data["statusCode"]
	response["headers"] = {}
	if "headers" in data:
		response["headers"] = data["headers"]
	response["body"] = json.dumps(data["body"])
	return response

def list_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))

def handler(event, context):
    print("Listing contents of /opt:")
    list_files('/opt')

    #S3_BUCKET = '10xshorts-storage-b043c5c4165946-staging'
    #SIGNED_URL_TIMEOUT = 60

    #body = json.loads(event['body'])
    body = event['body']
    #s3 = boto3.client('s3')

    #s3_source_signed_url = s3.generate_presigned_url('get_object',
    #    Params={'Bucket': S3_BUCKET, 'Key': 'private/eu-west-2:e28f9289-36d6-4b50-b641-37c1ea02e307/input_old.mp4'},
    #    ExpiresIn=SIGNED_URL_TIMEOUT)
    
    p1 = subprocess.run(["/opt/bin/ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(p1.stdout)

    #ffmpeg_cmd = "/opt/bin/ffmpeg -i " + s3_source_signed_url + " -ab 160k -ac 1 -ar 16000 -vn input.wav"
    #p1 = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print(p1.stdout)
    #resp = s3.put_object(Body=p1.stdout, Bucket=S3_BUCKET, Key="input.wav")

    response = {}
    response = {
    "isBase64Encoded": False,
    "statusCode": 200,
    "headers": {'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'},
    "body": body
    }

    return response_proxy(response)