import ffmpeg
import srt
from datetime import datetime
import os
import os.path
from os import listdir
import random

def animate_subtitle(video_input, audio_input, i, type, emoji_start, emoji_end):
    # emoji appear with popping sound
    if type==1:
        video_output = video_input.overlay(ffmpeg.input(temp_array[i][0]).filter("scale", int(90/404*width), int(90/404*width)), enable='between(t,'+emoji_start+','+emoji_end+')', x=(int(40/404*width)), y=(int(400/720*height)))
        delay = str(int(float(emoji_start)*1000))
        sound_pop_delay = ffmpeg.input('assets/sound_effects/pop.mp3').audio.filter("adelay",delays=str(delay)+"|"+str(delay)).output("files/pop_out_"+str(i)+".mp3").run(overwrite_output=True)
        sound_pop = ffmpeg.input("files/pop_out_"+str(i)+".mp3").audio
        audio_output = ffmpeg.filter([sound_pop, audio_input], 'amix', dropout_transition=0, normalize=0).filter("dynaudnorm")
    # emoji slides in from the left with whoosh
    elif type==2:
        video_output = video_input.overlay(ffmpeg.input(temp_array[i][0]).filter("scale", int(90/404*width), int(90/404*width)), enable='between(t,'+emoji_start+','+emoji_end+')', x="min(1000*(t"+"-"+str((datetime(1, 1, 1, 0, 0, 0, 0) + temp_array[i][2]).strftime("%S.%f"))+"),"+str(int(width/2)-32+110)+")", y=(int(400/720*height)))
        delay = str(int(float(emoji_start)*1000))
        sound_pop_delay = ffmpeg.input('assets/sound_effects/whoosh.mp3').audio.filter("adelay",delays=str(delay)+"|"+str(delay)).output("files/whoosh_out_"+str(i)+".mp3").run(overwrite_output=True)
        sound_pop = ffmpeg.input("files/whoosh_out_"+str(i)+".mp3").audio
        audio_output = ffmpeg.filter([sound_pop, audio_input], 'amix', dropout_transition=0, normalize=0).filter("dynaudnorm")
    elif type ==3:
        video_output = video_input.overlay(ffmpeg.input(temp_array[i][0]).filter("scale", int(90/404*width), int(90/404*width)), enable='between(t,'+emoji_start+','+emoji_end+')', x=int(50/404*width), y=400)
        audio_output = audio_input
    else:
        video_output = video_input.overlay(ffmpeg.input(temp_array[i][0]).filter("scale", int(64/404*width), int(64/404*width)).filter("rotate", a=10, fillcolor='none'), enable='between(t,'+emoji_start+','+emoji_end+')', x="100+10*(t"+"-"+str((datetime(1, 1, 1, 0, 0, 0, 0) + temp_array[i][2]).strftime("%S.%f"))+")", y=(int(100/720*height)))
    return video_output, audio_output

audio_stream = ffmpeg.input('files/output.mp4').audio

f = open("files/input.srt", "rt")
subtitles = f.read()
f.close()
subs = list(srt.parse(subtitles))

with open("files/emoji_array.txt") as file:
    emoji_array = [line.rstrip() for line in file]

temp_array = []

for i in range(len(emoji_array)):
    content = emoji_array[i].split(",")
    counter = content[0].count("U000")
    
    if counter == 1:
        string = content[0].split("U000")[1].split("'")[0]
    elif counter == 2:
        string = content[0].split("U000")[1].replace("\\\\","")+"-"+content[0].split("U000")[2].split("'")[0]
    else:
        string = "NA"

    probability = content[1].replace("]","")

    if string != "NA" and os.path.exists("assets/emoji_3D/"+string+".png") == True:
        temp_array.append(["assets/emoji_3D/"+string+".png", float(probability), subs[i].start, subs[i].end])

stream = ffmpeg.input('files/output.mp4')
probe = ffmpeg.probe('files/output.mp4')
video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
width = int(video_streams[0]['width'])
height = int(video_streams[0]['height'])

emoji_blacklist = []
for i in range(len(temp_array)):
    if temp_array[i][0] != "assets/emoji_3D/NA.png" and temp_array[i][1]>60 and temp_array[i][0] not in emoji_blacklist:
        emoji_start = str((datetime(1, 1, 1, 0, 0, 0, 0) + temp_array[i][2]).strftime("%S.%f"))
        emoji_end = str((datetime(1, 1, 1, 0, 0, 0, 0) + temp_array[i][3]).strftime("%S.%f"))
        animation_type = random.randint(1, 3)
        stream, audio_stream = animate_subtitle(stream, audio_stream, i, animation_type, emoji_start, emoji_end)
        emoji_blacklist.append(temp_array[i][0])
stream = stream.output(audio_stream, 'files/output_animations.mp4')
stream.run(overwrite_output=True)
  
folderPath = 'files/'
    
for fileName in listdir(folderPath):
    if fileName.endswith('.mp3'):
        os.remove(folderPath + fileName)