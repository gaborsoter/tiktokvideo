import ffmpeg
import random

#Define vars
video_path="files/garyvee.mp4"
subtitle_path = "files/clips/clip_0.srt"
audio = ffmpeg.input(video_path).audio

fonts_dir = "boldfont.otf"

stream = ffmpeg.input(video_path)

angles = ["-10", "0", "10"]

# concat subtitles
for i in range(31):
    subtitle_path = "files/clips/clip_"+str(i)+".srt"
    alignment = str(2)
    fontname = "Boldfont"
    outline = str(0)
    fontsize = str(10)
    shadow = str(1)
    marginL = str(100)
    marginR = str(100)
    marginV = str(100)
    randomangle = random.randint(0, 2)
    angle = angles[randomangle]
    color = "80ff80"
    style = "Alignment="+alignment+",FontName="+fontname+",Outline="+outline+",FontSize="+fontsize+",Shadow="+shadow+",MarginL="+marginL+",MarginR="+marginR+",MarginV="+marginV+",Angle="+angle+", PrimaryColour="+color
    stream = ffmpeg.concat(stream.filter("subtitles", subtitle_path, fontsdir=fonts_dir, force_style=style), audio, v=1, a=1)
stream.output("files/222.mp4").run()