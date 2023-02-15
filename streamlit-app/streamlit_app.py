import streamlit as st
import subprocess
import requests
import json
from pydub import AudioSegment
import os
import boto3
import botocore
import random
import ffmpeg
from subtitler import Subtitler
import base64

def upload_to_digital_ocean_space(file_name, file):
    # Upload file to Digital Ocean Spaces
    session = boto3.session.Session()
    client = session.client('s3',
                            endpoint_url='https://ams3.digitaloceanspaces.com', # Find your endpoint in the control panel, under Settings. Prepend "https://".
                            config=botocore.config.Config(s3={'addressing_style': 'virtual'}), # Configures to use subdomain/virtual calling format.
                            region_name='ams3', # Use the region in your endpoint.
                            aws_access_key_id='DO00AEDRKJUZK2F7V2DZ', # Access key pair. You can create access key pairs using the control panel or API.
                            aws_secret_access_key=os.getenv('SPACES_KEY')) # Secret access key defined through an environment variable.

    client.put_object(Bucket='tenxshorts', # The path to the directory you want to upload the object to, starting with your Space name.
                    Key=file_name, # Object key, referenced whenever you want to access this file later.
                    Body=file,
                    ACL='private', # Defines Access-control List (ACL) permissions, such as private or public.
                    Metadata={ # Defines metadata tags.
                        'x-amz-meta-my-key': 'your-value'
                    }
                    )

def export_audio(uploaded_file):
    str_one = "ffmpeg -i "
    str_two = " -ab 160k -ac 2 -ar 16000 -vn "
    command = str_one + uploaded_file.name + str_two + "input.mp4.wav"
    subprocess.call(command, shell=True)

def export_audio_from_memory(uploaded_file):
    args = (ffmpeg
            .input('pipe:', format='mp4')
            .output('pipe:', format='wav')
            .global_args('-analyzeduration', '2147483647', '-probesize', '2147483647', '-ab', '160k', '-ac', '1', '-ar', '16000', '-vn')
            .get_args()
            )
    # print(args)
    proc = subprocess.Popen(
        ['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    return proc.communicate(input=uploaded_file.getvalue())[0]

st.write("Hello world") 

# give me a random hex name with 20 digits
random_name = str(random.getrandbits(80))

uploaded_file = st.file_uploader("Upload Files",type=['mp4'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

    upload_to_digital_ocean_space(random_name + ".mp4", uploaded_file)

    audio = export_audio_from_memory(uploaded_file)

    upload_to_digital_ocean_space(random_name + ".wav", audio)
    st.write("audio written to file")

    if st.button('Create transcript'):
        st.write('Creating transcript...')
        subtitler = Subtitler()
        
        subtitler(audio)
        st.write('Transcript created!')

    

    #try:
    #    os.remove("input.mp4.wav")
    #except:
    #    pass