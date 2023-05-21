import os
import requests
import json
from deepgram import Deepgram
from decouple import config

DEEPGRAM_API_KEY = config('DEEPGRAM_API_KEY')

PATH_TO_FILE = 'files/input.wav'
MIMETYPE = 'audio/wav'

dg_client = Deepgram(DEEPGRAM_API_KEY)

def format_time(time):
    time = float(time)
    hours = int(time // 3600)
    minutes = int((time // 60) % 60)
    seconds = int(time % 60)
    milliseconds = int((time - int(time)) * 1000)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(hours, minutes, seconds, milliseconds)

def create_srt_file(data, filename):
    srt_file = open(filename, 'w')
    count = 1
    for i in range(len(data)):
        srt_file.write(str(count) + '\n')
        start_time = "{:.3f}".format(data[i]['start'])
        end_time = "{:.3f}".format(data[i]['end'])
        srt_file.write(format_time(start_time) + ' --> ' + format_time(end_time) + '\n')
        srt_file.write(data[i]['punctuated_word'] + '\n\n')
        count += 1
    srt_file.close()

with open(PATH_TO_FILE, 'rb') as audio:
    source = {'buffer': audio, 'mimetype': MIMETYPE}
    options = { "punctuate": True, "model": "nova", "language": "en-US" }

    response = dg_client.transcription.sync_prerecorded(source, options)
    response = json.dumps(response)
    response = json.loads(response)

    json_data = response["results"]["channels"][0]["alternatives"][0]["words"]
    filename = "files/caption.srt"
    create_srt_file(json_data, filename)

    transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]

    transcript_file = open("files/transcript.txt", "w")
    transcript_file.write(transcript)
    transcript_file.close()
