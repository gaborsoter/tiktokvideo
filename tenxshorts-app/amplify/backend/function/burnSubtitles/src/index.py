import json
import boto3
import ffmpeg
import os
import os.path
import urllib3
import srt
import random
import io
import subprocess

def sort_key(file):
    # We split by underscore '_' and take the last part
    # Then we remove the '.mp4' and convert the rest to an integer
    return int(file.split('clip_')[-1].replace('.srt', ''))

def response_proxy(data):
	response = {}
	response["isBase64Encoded"] = False
	response["statusCode"] = data["statusCode"]
	response["headers"] = {}
	if "headers" in data:
		response["headers"] = data["headers"]
	response["body"] = json.dumps(data["body"])
	return response

def calculate_font_size(value):
    # min and max character length
    leftMin = 0
    leftMax = 15

    # min and max font size
    rightMin = 40
    rightMax = 15

    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

def list_files(s3, bucket_name, prefix):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = []
    for obj in response['Contents']:
        files.append(obj['Key'])
    return files

def animate_subtitle(type, subtitle_path, current_bit_length, colour, font_size, caps, s3, S3_BUCKET, SIGNED_URL_TIMEOUT):
        print("CURRENT BIT LENGTH: ", current_bit_length)
        s3_source_signed_url = s3.generate_presigned_url('get_object',
            Params={'Bucket': S3_BUCKET, 'Key': subtitle_path},
            ExpiresIn=SIGNED_URL_TIMEOUT)
        http = urllib3.PoolManager()
        response = http.request('GET', s3_source_signed_url)
        print("subtitle_path: ", subtitle_path)
        subtitle = response.data.decode('utf-8')
        
        subtitle = list(srt.parse(subtitle))

        if colour == "red":
            subtitle_colour = "#D7090E"
        elif colour == "green":
            subtitle_colour = "#36FE1E"
        elif colour == "biobubi":
            subtitle_colour = "#4EABA4"
        else:
            subtitle_colour = "#FAFF00"



        # Do nothing
        if type==-1:
            temp_content = subtitle[0].content.split(" ")

            division_point = int(len(temp_content)/2)
            


            temp_content.insert(division_point, "\n")
            subtitle[0].content = '<font color="#FFFFFF" size="'+str(font_size)+'">' + ' '.join(temp_content[:division_point]) + " " + '</font>' + '<font color="#FFFFFF" size="'+str(font_size)+'">' + ' '.join(temp_content[division_point:]) + '</font>'
            subtitle = srt.compose(subtitle)

        # Change colour for the whole subtitle
        if type==0:
            temp_content = subtitle[0].content.split(" ")

            division_point = int(len(temp_content)/2)
            temp_content.insert(division_point, "\n")
            subtitle[0].content = '<font color="#FAFF00" size="'+str(font_size)+'">' + ' '.join(temp_content[:division_point]) + " " + '</font>' + '<font color="#FAFF00" size="'+str(font_size)+'">' + ' '.join(temp_content[division_point:]) + '</font>'
            subtitle = srt.compose(subtitle)

        # Change colour only for the second part of the subtitle
        if type==1:
            temp_content = subtitle[0].content.split(" ")

            division_point = int(len(temp_content)/2)
            temp_content.insert(division_point, "\n")

            subtitle[0].content = '<font color="#FFFFFF" size="'+str(font_size)+'">' + ' '.join(temp_content[:division_point]) + " " + '</font>' + '<font color="#FAFF00" size="'+str(font_size)+'">' + ' '.join(temp_content[division_point:]) + '</font>'
            subtitle = srt.compose(subtitle)

        # Split the subtitle into words
        if type==2:
            temp_content = subtitle[0].content.split(" ")
            new_subtitles = []
            for i in range(len(temp_content)):
                content = caps[current_bit_length+i].content
                font_size = calculate_font_size(len(content))
                content = '<font color='+subtitle_colour+' size="'+str(font_size)+'">' + str(content) + '</font>'

                print("CONTENT: ", content)
                new_subtitles.append(srt.Subtitle(index=i+1, start=caps[current_bit_length+i].start, 
                                end=caps[current_bit_length+i].end, 
                                content=content, proprietary=''))

            subtitle = srt.compose(new_subtitles)

        # Colour only the word that is spoken
        if type==3:
            print(subtitle)
            temp_content = subtitle[0].content.split(" ")
            print("TEMP_CONTENT: ", temp_content)
            print("CAPS: ", caps)
            
            new_subtitles = []
            for i in range(len(temp_content)):
                print("END: ", caps[current_bit_length+i])
                if i==0:
                    content = '<font color='+subtitle_colour+' size="'+str(font_size)+'">' + "".join(temp_content[i]) + " " + '</font>' + '<font color="#FFFFFF" size="'+str(font_size)+'">' + " ".join(temp_content[i+1:]) + '</font>'
                elif i==(len(temp_content)-1):
                    content = '<font color="#FFFFFF" size="'+str(font_size)+'">' + " ".join(temp_content[:i]) + '</font>' + '<font color='+subtitle_colour+' size="'+str(font_size)+'">' + " " + "".join(temp_content[i]) + '</font>'
                else:
                    content = '<font color="#FFFFFF" size="'+str(font_size)+'">' + " ".join(temp_content[:i]) + '</font>' + '<font color='+subtitle_colour+' size="'+str(font_size)+'">' + " " + "".join(temp_content[i]) + " " + '</font>' + '<font color="#FFFFFF" size="'+str(font_size)+'">' + " ".join(temp_content[i+1:]) + '</font>'
                if (current_bit_length+i+1>(len(caps)-1)):
                    end = caps[current_bit_length+i].end
                else:
                    end = caps[current_bit_length+i+1].start
                new_subtitles.append(srt.Subtitle(index=i+1, start=caps[current_bit_length+i].start, 
                                end=end, 
                                content=content, proprietary=''))

            subtitle = srt.compose(new_subtitles)

        print("putobjectabove")
        s3.put_object(Body=subtitle, Bucket=S3_BUCKET, Key=subtitle_path)
        print("putobjectbelow")

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

    S3_BUCKET = '10xshorts-storage-b043c5c4165946-staging'
    SIGNED_URL_TIMEOUT = 600
    s3 = boto3.client('s3')

    fonts_dir = "./fonts/" # this needs to be changed

    filename_transcript_bit_length = os.path.splitext(filename)[0] + '_bit_lengths' + '.txt'
    s3_source_signed_url = s3.generate_presigned_url('get_object',
        Params={'Bucket': S3_BUCKET, 'Key': 'private/' + user_id + '/' + filename_transcript_bit_length},
        ExpiresIn=SIGNED_URL_TIMEOUT)
    http = urllib3.PoolManager()
    response = http.request('GET', s3_source_signed_url)
    file_content = response.data.decode('utf-8')

    content_list = file_content.split(",")
    content_list[0] = content_list[0].replace('[', '')
    content_list[-1] = content_list[-1].replace(']', '')
    bit_lengths= [int(x) for x in content_list]

    filename_caption = os.path.splitext(filename)[0] + '_caption.srt'
    s3_source_signed_url = s3.generate_presigned_url('get_object',
        Params={'Bucket': S3_BUCKET, 'Key': 'private/' + user_id + '/' + filename_caption},
        ExpiresIn=SIGNED_URL_TIMEOUT)
    http = urllib3.PoolManager()
    response = http.request('GET', s3_source_signed_url)
    captions = response.data.decode('utf-8')

    caps = list(srt.parse(captions))
    print("Caps:", caps)


    angles = ["-10", "0", "10"]
    colour = ["red", "green", "yellow"]

    colour.append("red")
    colour.append("green")

    i = 0

    # List all files in S3 folder
    prefix = 'private/' + user_id + '/' + os.path.splitext(filename)[0] + '_clips'
    subtitle_paths = list_files(s3, S3_BUCKET, prefix)

    # remove the first item
    subtitle_paths.pop(0)

    subtitle_paths = sorted(subtitle_paths, key=sort_key)

    print("SUBTITLE PATHS: ", subtitle_paths)
    lambda_client = boto3.client('lambda')

    # check whether there is a folder in S3 if not create a folder
    try:
        s3.head_object(Bucket=S3_BUCKET, Key='private/' + user_id + '/' + os.path.splitext(filename)[0] + '_videoclips/')
    except:
        s3.put_object(Bucket=S3_BUCKET, Key='private/' + user_id + '/' + os.path.splitext(filename)[0] + '_videoclips/')


    number_of_subtitles = len(subtitle_paths)
    #number_of_subtitles = 2
    for i in range(number_of_subtitles):
        print("ITERATION: ", i)
        
        subtitle_path = subtitle_paths[i]
        #animation_type = random.randint(2, 3)
        animation_type = 3
        sub_colour = "yellow"
        fontsize = str(20)
        animate_subtitle(animation_type, subtitle_path, bit_lengths[i], sub_colour, fontsize, caps, s3, S3_BUCKET, SIGNED_URL_TIMEOUT)
        alignment = str(2)
        fontname = "My Font"
        outline = str(0)
        shadow = str(1)
        marginL = str(100)
        marginR = str(100)
        marginV = str(50)
        randomangle = random.randint(0, 2)
        angle = angles[randomangle]
        #angle = str(0)
        color = "80ff80"
        style = "Alignment="+alignment+",FontName="+fontname+",Outline="+outline+",FontSize="+fontsize+",Shadow="+shadow+",MarginL="+marginL+",MarginR="+marginR+",MarginV="+marginV+",Angle="+angle+", PrimaryColour="+color
        
        s3_source_signed_url = s3.generate_presigned_url('get_object',
        Params={'Bucket': S3_BUCKET, 'Key': subtitle_path},
        ExpiresIn=SIGNED_URL_TIMEOUT)

        response = http.request('GET', s3_source_signed_url)
        subtitles = response.data.decode('utf-8')

        subtitle_list = list(srt.parse(subtitles))
        print("Subtitle list:", subtitle_list)

        if i == 0:
            clip_start = "00.000"
        else:
            clip_start = clip_end

        clip_end = subtitle_list[-1].end
        clip_end_total_seconds = clip_end.total_seconds()
        clip_end = "{:.3f}".format(clip_end_total_seconds)

        payload = {
        'clip_start': clip_start,
        'clip_end': clip_end,
        'temp_subtitle': subtitles,
        'user_id': user_id,
        'filename': filename,
        'S3_bucket': S3_BUCKET,
        'iteration': i,
        'number_of_subtitles': number_of_subtitles,
        'fonts_dir': fonts_dir,
        'style': style,
        }

        response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:eu-west-2:254108557594:function:burnSubtitlesSegment-staging',
            InvocationType='Event',
            Payload=json.dumps(payload),
        )

    

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