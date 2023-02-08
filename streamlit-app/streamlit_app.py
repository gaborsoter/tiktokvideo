import streamlit as st
import subprocess
import requests
import json
from pydub import AudioSegment
import os
import boto3
import botocore
import random

def export_audio(uploaded_file):
    str_one = "ffmpeg -i "
    str_two = " -ab 160k -ac 2 -ar 16000 -vn "
    command = str_one + uploaded_file.name + str_two + "input.mp4.wav"
    subprocess.call(command, shell=True)

st.write("Hello world") 

# give me a random hex name with 20 digits
random_name = str(random.getrandbits(80))

uploaded_file = st.file_uploader("Upload Files",type=['mp4'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

    session = boto3.session.Session()
    client = session.client('s3',
                            endpoint_url='https://ams3.digitaloceanspaces.com', # Find your endpoint in the control panel, under Settings. Prepend "https://".
                            config=botocore.config.Config(s3={'addressing_style': 'virtual'}), # Configures to use subdomain/virtual calling format.
                            region_name='ams3', # Use the region in your endpoint.
                            aws_access_key_id='DO00AEDRKJUZK2F7V2DZ', # Access key pair. You can create access key pairs using the control panel or API.
                            aws_secret_access_key=os.getenv('SPACES_KEY')) # Secret access key defined through an environment variable.

    # Step 3: Call the put_object command and specify the file to upload.
    client.put_object(Bucket='tenxshorts', # The path to the directory you want to upload the object to, starting with your Space name.
                    Key=random_name + ".mp4", # Object key, referenced whenever you want to access this file later.
                    Body=uploaded_file,
                    ACL='private', # Defines Access-control List (ACL) permissions, such as private or public.
                    Metadata={ # Defines metadata tags.
                        'x-amz-meta-my-key': 'your-value'
                    }
                    )

    #export_audio(uploaded_file)

    #sound = AudioSegment.from_wav("input.mp4.wav")
    #sound = sound.set_channels(1)
    #sound.export("input.wav", format="wav")

    #try:
    #    os.remove("input.mp4.wav")
    #except:
    #    pass