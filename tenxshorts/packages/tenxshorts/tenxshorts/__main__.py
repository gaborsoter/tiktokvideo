import subprocess
import requests
import json
from pydub import AudioSegment
import os

#input_file_path = "files/input.mp4"

def export_audio(input_file_path):
	'''
	str_one = "ffmpeg -i "
	str_two = " -ab 160k -ac 2 -ar 16000 -vn "
	str_three = ".wav"
	input_name = input_file_path.split(". ")[0]
	command = str_one + input_file_path + str_two + input_name + str_three 
	subprocess.call(command, shell=True)
	'''
	return

def main(args):
	input_file_path = ""
	export_audio(input_file_path)
	'''
	sound = AudioSegment.from_wav("files/input.mp4.wav")
	sound = sound.set_channels(1)
	sound.export("files/input.wav", format="wav")

	try:
    	    os.remove("files/input.mp4.wav")
	except:
        pass
	return {"body": "Hello World!"}
	'''
	return {"body": "Hello World!"}

