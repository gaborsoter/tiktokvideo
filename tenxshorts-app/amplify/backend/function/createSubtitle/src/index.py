import json
import os
import openai
import boto3
import urllib3
import re
import srt
import json
import sys
import asyncio
import aiohttp
import ast

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

    # OpenAI Setup
    ssm = boto3.client('ssm')
    parameter_name = '/amplify/d2z1h6fuy2vpsk/staging/AMPLIFY_createSubtitle_OPENAI_API_KEY'
    with_decryption = True
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=with_decryption)
    OPENAI_API_KEY = response['Parameter']['Value']

    # Get file from S3
    S3_BUCKET = '10xshorts-storage-b043c5c4165946-staging'
    SIGNED_URL_TIMEOUT = 180
    s3 = boto3.client('s3')
    filename_transcript = os.path.splitext(filename)[0] + '.txt'
    s3_source_signed_url = s3.generate_presigned_url('get_object',
        Params={'Bucket': S3_BUCKET, 'Key': 'private/' + user_id + '/' + filename_transcript},
        ExpiresIn=SIGNED_URL_TIMEOUT)
    http = urllib3.PoolManager()
    response = http.request('GET', s3_source_signed_url)
    data = response.data.decode('utf-8')

    data = data.replace('. ', '._END_')
    phrases = data.split('_END_')
    data_list = []

    instruction = "Split the sentences into smaller chunks such that the chunks don't have more than 6 words. Here are a few examples:\n\nInput: Welcome to Larry King Now. Our special guest is Gary Vaynerchuk. \n\n[\"Welcome to Larry King Now.\", \"Our special guest is Gary Vaynerchuk.\"]\n\nInput: The self-proclaimed hustler is a digital media mogul, author, web show host, and venture capitalist, among many other things.\n\n[\"The self-proclaimed hustler\", \"is a digital media mogul\", \"author, web show host\", \"and venture capitalist,\", \"among many other things.\"]\n\nInput: As the CEO and co-founder of VaynerMedia, Gary hosts the hugely popular YouTube show, Ask Gary Vee, and has penned three New York Times bestselling books.\n\n[\"As the CEO and\", \"co-founder of VaynerMedia,\", \"Gary hosts the hugely popular\", \"YouTube show, Ask Gary Vee,\", \"and has penned three\", \"New York Times bestselling books.\"]\n\nInput: "
    
    # create paragraphs from phrases that are no longer than 600 characters
    paragraphs = []
    length_of_paragraph = 0
    current_paragraph = ""
    for phrase in phrases:
        if length_of_paragraph < 600:
            current_paragraph += " " + phrase
            length_of_paragraph += len(phrase)
        else:
            paragraphs.append(current_paragraph)
            current_paragraph = phrase
            length_of_paragraph = len(phrase)

    paragraphs.append(current_paragraph)

    for paragraph in paragraphs:
        data_list.append({"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": instruction + paragraph}], "temperature": 0})

    print(paragraph)

    conn = aiohttp.TCPConnector(limit_per_host=10, limit=0, ttl_dns_cache=300)
    PARALLEL_REQUESTS = 100
    results = [{} for _ in range(len(data_list))]  # initialize with empty dictionaries
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    async def gather_with_concurrency(n, data_list):
        semaphore = asyncio.Semaphore(n)
        session = aiohttp.ClientSession(connector=conn)

        async def post(index, data):
            async with semaphore:
                async with session.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data) as response:
                    obj = json.loads(await response.read())
                    results[index] = obj

        await asyncio.gather(*(post(i, data) for i, data in enumerate(data_list)))
        await session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather_with_concurrency(PARALLEL_REQUESTS, data_list))
    conn.close()

    print(results)

    async_results = []

    for i in range(len(results)):
        temp_result = json.loads(results[i]["choices"][0]["message"]["content"])
        async_results.append(temp_result)

    bits = [num for sublist in async_results for num in sublist]

    # Upload audio to S3
    file_content = '\n'.join(bits)
    
    # Upload the file to S3
    key = 'private/' + user_id + '/' + os.path.splitext(filename)[0] + '_bits.txt'
    resp = s3.put_object(Body=file_content, Bucket=S3_BUCKET, Key=key)

    # Get subtitle file from S3
    S3_BUCKET = '10xshorts-storage-b043c5c4165946-staging'
    filename_transcript = os.path.splitext(filename)[0] + '_caption.srt'
    s3_source_signed_url = s3.generate_presigned_url('get_object',
        Params={'Bucket': S3_BUCKET, 'Key': 'private/' + user_id + '/' + filename_transcript},
        ExpiresIn=SIGNED_URL_TIMEOUT)
    http = urllib3.PoolManager()
    response = http.request('GET', s3_source_signed_url)
    subtitles = response.data.decode('utf-8')

    subs = list(srt.parse(subtitles))

    bitsubs = []

    bit_index = 1

    sub_index = 0

    bit_lengths = []
    total_bit_length = 0

    for bit in bits:
        length_of_bit = len(bit.split(" "))
        bit_lengths.append(total_bit_length)
        total_bit_length += length_of_bit

        bitsubs.append(srt.Subtitle(index=bit_index, start=subs[sub_index].start, 
                                    end=subs[sub_index + length_of_bit - 1].end, 
                                    content=bit, proprietary=''))

        sub_index += length_of_bit
        bit_index += 1

    # Upload the file to S3
    key = 'private/' + user_id + '/' + os.path.splitext(filename)[0] + '.srt'
    resp = s3.put_object(Body=srt.compose(bitsubs), Bucket=S3_BUCKET, Key=key)

    key = 'private/' + user_id + '/' + os.path.splitext(filename)[0] + '_bit_lengths.txt'
    resp = s3.put_object(Body=json.dumps(bit_lengths), Bucket=S3_BUCKET, Key=key)

    filename_subtitle = os.path.splitext(filename)[0] + '.srt'
    s3_source_signed_url = s3.generate_presigned_url('get_object',
        Params={'Bucket': S3_BUCKET, 'Key': 'private/' + user_id + '/' + filename_subtitle},
        ExpiresIn=SIGNED_URL_TIMEOUT)
    http = urllib3.PoolManager()
    response = http.request('GET', s3_source_signed_url)
    subtitles = response.data.decode('utf-8')

    subs = list(srt.parse(subtitles))

    # Exporting subtitle files
    for i in range(len(subs)):
        temp_sub = srt.Subtitle(index=1, start=subs[i].start, 
                                    end=subs[i].end, 
                                    content=subs[i].content.upper(), proprietary='')

        temp_sub = srt.compose([temp_sub])

        # check whether there is a folder in S3 if not create a folder
        try:
            s3.head_object(Bucket=S3_BUCKET, Key='private/' + user_id + '/' + os.path.splitext(filename)[0] + '_clips/')
        except:
            s3.put_object(Bucket=S3_BUCKET, Key='private/' + user_id + '/' + os.path.splitext(filename)[0] + '_clips/')


        key = 'private/' + user_id + '/' + os.path.splitext(filename)[0] + '_clips/' + 'clip_'+str(i)+'.srt'
        resp = s3.put_object(Body=temp_sub, Bucket=S3_BUCKET, Key=key)

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