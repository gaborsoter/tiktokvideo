
import srt
import datetime
import subprocess
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from customSubtitles import CustomSubtitlesClip
from customTextClip import CustomTextClip

def generate_subtitle(subtitle_number):
    shadow_dist = int(fontsize/10)
    temp_generator_shadow = lambda txt: CustomTextClip(txt, font='Boldfont-Bold', fontsize=50, color='black', rotate=10, align = "center")
    temp_subtitles_shadow = CustomSubtitlesClip("files/clips/clip_"+str(subtitle_number)+".srt", temp_generator_shadow).set_pos(("center", int(height*2/3) + shadow_dist))
    temp_generator = lambda txt: CustomTextClip(txt, font='Boldfont-Bold', fontsize=50, color='white', rotate=10, align = "center")
    temp_subtitles = CustomSubtitlesClip("files/clips/clip_"+str(subtitle_number)+".srt", temp_generator)
    return temp_subtitles_shadow, temp_subtitles

fontsize = 50

video = VideoFileClip("files/garyvee.mp4")
width, height = video.size
duration = str(video.duration)
seconds = duration.split(".")[0]
milliseconds = duration.split(".")[1]

f = open("files/garyvee.srt", "rt")
subtitles = f.read()
f.close()

subs = list(srt.parse(subtitles))

# Exporting subtitle files
for i in range(len(subs)):
    temp_sub = srt.Subtitle(index=1, start=subs[i].start, 
                                end=subs[i].end, 
                                content=subs[i].content, proprietary='')

    temp_sub = srt.compose([temp_sub])

    CAPTION_FILE = open("files/clips/clip_"+str(i)+".srt", "w")
    CAPTION_FILE.write(temp_sub)
    CAPTION_FILE.close()
    
temp_result = video
# Add subtitles to clips
for i in range(len(subs)):
    temp_subtitles_shadow, temp_subtitles = generate_subtitle(i)
    temp_shadow = CompositeVideoClip([temp_result, temp_subtitles_shadow])
    temp_result = CompositeVideoClip([temp_shadow, temp_subtitles])

temp_result.write_videofile("files/clips/final.mp4", fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec = "mpeg4", audio_codec="aac")

'''
generator_shadow = lambda txt: CustomTextClip(txt, font='Boldfont-Bold', fontsize=50, color='black', rotate=10, align = "center")
subtitles_shadow = CustomSubtitlesClip("files/garyvee.srt", generator_shadow).set_pos(("center", int(height*2/3) + shadow_dist))

generator = lambda txt: CustomTextClip(txt, font='Boldfont-Bold', fontsize=50, color='white', rotate=10, align = "center")
subtitles = CustomSubtitlesClip("files/garyvee.srt", generator)

shadow = CompositeVideoClip([video, subtitles.set_pos(("center", int(height*2/3)))])
result = CompositeVideoClip([shadow, subtitles.set_pos(("center", int(height*2/3)))])

result.write_videofile("files/beauty-garyvee.mp4", fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
'''