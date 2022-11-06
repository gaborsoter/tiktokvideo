import subprocess
import requests
import json
import replicate

REPLICATE_TOKEN = "1fd8380427d84aee93a27b0def46d4930dabac0b"

input_file_path = "./files/garyvee.mp4"

def export_audio(input_file_path):
    str_one = "ffmpeg -i "w
    str_two = " -ab 160k -ac 2 -ar 44100 -vn "
    str_three = ".wav"
    input_name = input_file_path.split(". ")[0]
    command = str_one + input_file_path + str_two + input_name + str_three 
    subprocess.call(command, shell=True)

def transcribe_audio(input_file_path):
    with open(input_file_path+".wav", 'rb') as f:
        model = replicate.models.get("openai/whisper")
        output = model.predict(audio=f)
        return output

export_audio(input_file_path)
response = transcribe_audio(input_file_path)

with open(input_file_path+'.json', 'w') as f:
    json.dump(response, f)