import streamlit as st
import subprocess
import requests
import json
from pydub import AudioSegment
import os

def export_audio(uploaded_file):
    str_one = "ffmpeg -i "
    str_two = " -ab 160k -ac 2 -ar 16000 -vn "
    command = str_one + uploaded_file.name + str_two + "input.mp4.wav"
    subprocess.call(command, shell=True)

st.write("Hello world") 

uploaded_file = st.file_uploader("Upload Files",type=['mp4'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

    export_audio(uploaded_file)

    #sound = AudioSegment.from_wav("input.mp4.wav")
    #sound = sound.set_channels(1)
    #sound.export("input.wav", format="wav")

    #try:
    #    os.remove("input.mp4.wav")
    #except:
    #    pass

