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
    S3_BUCKET = '10xshorts-storage-b043c5c4165946-staging'
    SIGNED_URL_TIMEOUT = 60

    # Get payload from request
    body = json.loads(event['body'])
    filename = body['videoKey']

    # Get user ID from Cognito
    identity_id = event['requestContext']['authorizer']['claims']['cognito:username']
    client = boto3.client('cognito-idp')
    user_pool_id = 'eu-west-2_wYUHJ7g30'
    filter = f'sub = "{identity_id}"'
    response = client.list_users(
        UserPoolId=user_pool_id,
        Filter=filter
    )
    user = response['Users'][0]
    user_id = user['Attributes']
    user_id = next((d['Value'] for d in user_id if d['Name'] == 'address'), None) # Address is the custom attribute that stores the user ID

    # Get file from S3
    s3 = boto3.client('s3')

    s3_source_signed_url = s3.generate_presigned_url('get_object',
        Params={'Bucket': S3_BUCKET, 'Key': 'private/' + user_id + '/' + filename},
        ExpiresIn=SIGNED_URL_TIMEOUT)
    
    # Convert video to audio
    ffmpeg_cmd = "/opt/bin/ffmpeg -i \"" + s3_source_signed_url + "\" -f wav -ab 160k -ac 1 -ar 16000 -vn -"
    command1 = shlex.split(ffmpeg_cmd)
    p1 = subprocess.run(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Replace the filename extension with .wav
    filename_audio = os.path.splitext(filename)[0] + '.wav'

    # Upload audio to S3
    key = 'private/' + user_id + '/' + filename_audio
    resp = s3.put_object(Body=p1.stdout, Bucket=S3_BUCKET, Key=key)

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