import json
import ffmpeg
import subprocess
import boto3
import os
from io import BytesIO

def sort_key(file):
    # We split by underscore '_' and take the last part
    # Then we remove the '.mp4' and convert the rest to an integer
    return int(file.split('_')[-1].replace('.mp4', ''))

def handler(event, context):

    print("OS check")
    # list all files in /tmp
    print(os.listdir('/tmp'))
    print("OS check done")


    # extract payload from events and initialize variables
    clip_start = event['clip_start']
    clip_end = event['clip_end']
    temp_subtitle = event['temp_subtitle']
    user_id = event['user_id']
    filename = event['filename']
    S3_BUCKET = event['S3_bucket']
    i = event['iteration']
    number_of_subtitles = event['number_of_subtitles']
    fonts_dir = event['fonts_dir']
    style = event['style']

    s3 = boto3.client('s3')

    s3_source_signed_url_video = s3.generate_presigned_url('get_object',
    Params={'Bucket': S3_BUCKET, 'Key': 'private/' + user_id + '/' + filename},
    ExpiresIn=600)

    # write subtitles to file
    with open('/tmp/temp_subtitle.srt', 'w') as f:
        f.write(temp_subtitle)

    stream = ffmpeg.input(s3_source_signed_url_video)
    audio = ffmpeg.input(s3_source_signed_url_video).audio

    print("CLIP START END: ",clip_start, clip_end)
    stream = ffmpeg.concat(stream.filter("subtitles", "/tmp/temp_subtitle.srt", fontsdir=fonts_dir, force_style=style), audio, v=1, a=1)
    stream.output("/tmp/output.mp4").run(overwrite_output=True)



    command = [
        'python3',
        '-m',
        'ffmpeg_smart_trim.trim',
        '/tmp/output.mp4',
        '--start_time',
        clip_start,
        '--end_time',
        clip_end,
        '--output',
        '/tmp/output_cut.mp4'
    ]

    print("SUBPROCESS STARTED")
    subprocess.run(command)
    

    print("UPLOAD S3")
    # Upload the file to S3
    key = 'private/' + user_id + '/' + os.path.splitext(filename)[0]  + '_videoclips' + '/' + 'out_' + str(i) + '.mp4'
    with open('/tmp/output_cut.mp4', 'rb') as f:
        s3.upload_fileobj(f, S3_BUCKET, key)

    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(S3_BUCKET)
    number_of_files = 0

    list_of_files = []
    for _ in bucket.objects.filter(Prefix='private/' + user_id + '/' + os.path.splitext(filename)[0]  + '_videoclips' + '/'):
        number_of_files += 1
        list_of_files.append(_.key)
        print("FILE: ", _.key)

    number_of_files -= 1
    list_of_files.pop(0)

    list_of_files = sorted(list_of_files, key=sort_key)

    print("LIST OF FILES: ", list_of_files)
    
    print("NUMBER OF FILES: ", number_of_files)
    if number_of_files == number_of_subtitles:
        # write list_of_files of files to file
        videos = []
        for key in list_of_files:
            print("KEY: ", key)
            obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
            videos.append(BytesIO(obj['Body'].read()))

        # Write videos to temporary files
        temp_files = []
        for i, video in enumerate(videos):
            temp_file = f'/tmp/video_clip{i}.mp4'
            with open(temp_file, 'wb') as f:
                f.write(video.getvalue())
            temp_files.append(temp_file)

        print("TEMP FILES: ", len(temp_files))
        
        print("MERGING STARTED")
        # Merge videos using ffmpeg
        # Prepare filter_complex argument
        inputs = ''.join([f'-i {temp_file} ' for temp_file in temp_files])
        filter_complex = '"[' + ']['.join(f'{i}:v] [{i}:a' for i in range(len(temp_files))) + \
                        f']concat=n={len(temp_files)}:v=1:a=1 [v] [a]"'

        # Merge videos using ffmpeg
        output_file = '/tmp/output_final.mp4'
        command = f'ffmpeg -y {inputs} -vsync passthrough -filter_complex {filter_complex} -map "[v]" -map "[a]" {output_file}'
        subprocess.call(command, shell=True)

    
        # Upload the file to S3
        key = 'private/' + user_id + '/' + os.path.splitext(filename)[0] + '_final' + '.mp4'
        with open('/tmp/output_final.mp4', 'rb') as f:
            s3.upload_fileobj(f, S3_BUCKET, key)
    

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Hello from your new Amplify Python lambda!')
    }