import streamlit as st
import subprocess
import requests
import json
from pydub import AudioSegment
import os

st.write("Hello world") 

uploaded_file = st.file_uploader("Upload Files",type=['mp4'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)


input_file_path = "uploaded_file"

def export_audio(input_file_path):
    str_one = "ffmpeg -i "
    str_two = " -ab 160k -ac 2 -ar 16000 -vn "
    str_three = ".wav"
    input_name = input_file_path.split(". ")[0]
    command = str_one + input_file_path + str_two + input_name + str_three 
    subprocess.call(command, shell=True)

export_audio(input_file_path)

sound = AudioSegment.from_wav("files/input.mp4.wav")
sound = sound.set_channels(1)
sound.export("files/input.wav", format="wav")

try:
    os.remove("files/input.mp4.wav")
except:
    pass