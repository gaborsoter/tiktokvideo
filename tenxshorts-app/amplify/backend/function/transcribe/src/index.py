import json
import boto3
import os
import json
from deepgram import Deepgram

def format_time(time):
    time = float(time)
    hours = int(time // 3600)
    minutes = int((time // 60) % 60)
    seconds = int(time % 60)
    milliseconds = int((time - int(time)) * 1000)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(hours, minutes, seconds, milliseconds)

def create_srt_file(data):
    srt_file = ''
    count = 1
    for i in range(len(data)):
        srt_file += str(count) + '\n'
        start_time = "{:.3f}".format(data[i]['start'])
        end_time = "{:.3f}".format(data[i]['end'])
        srt_file += format_time(start_time) + ' --> ' + format_time(end_time) + '\n'
        srt_file += data[i]['punctuated_word'] + '\n\n'
        count += 1
        
    return srt_file

def response_proxy(data):
	response = {}
	response["isBase64Encoded"] = False
	response["statusCode"] = data["statusCode"]
	response["headers"] = {}
	if "headers" in data:
		response["headers"] = data["headers"]
	response["body"] = json.dumps(data["body"])
	return response

def handler(event, context):
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
    S3_BUCKET = '10xshorts-storage-b043c5c4165946-staging'
    SIGNED_URL_TIMEOUT = 60
    s3 = boto3.client('s3')

    filename_audio = os.path.splitext(filename)[0] + '.wav'

    s3_source_signed_url = s3.generate_presigned_url('get_object',
        Params={'Bucket': S3_BUCKET, 'Key': 'private/' + user_id + '/' + filename_audio},
        ExpiresIn=SIGNED_URL_TIMEOUT)
    
    # Create an SSM client
    ssm = boto3.client('ssm')

    # Set up the parameter request
    parameter_name = '/amplify/d2z1h6fuy2vpsk/staging/AMPLIFY_transcribe_deepgram_api_key'
    with_decryption = True # Retrieve the decrypted value of the parameter

    # Retrieve the parameter from the SSM Parameter Store
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=with_decryption)

    # Use the parameter in your code
    my_secret = response['Parameter']['Value']

    # Create transcript
    dg_client = Deepgram(my_secret)
    source = {'url': s3_source_signed_url}
    options = { "punctuate": True, "model": "nova", "language": "en-US" }

    transcript_response = dg_client.transcription.sync_prerecorded(source, options)
    transcript_response = json.dumps(transcript_response)
    transcript_response = json.loads(transcript_response)

    transcript = transcript_response["results"]["channels"][0]["alternatives"][0]["transcript"]    
    # Upload transcript to S3
    filename_transcript = os.path.splitext(filename)[0] + '.txt'
    key = 'private/' + user_id + '/' + filename_transcript
    s3.put_object(Body=transcript, Bucket=S3_BUCKET, Key=key)
    
    # Create SRT file
    words = transcript_response["results"]["channels"][0]["alternatives"][0]["words"] 
    srt_file = create_srt_file(words)

    filename_caption = os.path.splitext(filename)[0] + '_caption.srt'
    key = 'private/' + user_id + '/' + filename_caption
    s3.put_object(Body=srt_file, Bucket=S3_BUCKET, Key=key)

    print(key)

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