from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from customSubtitles import CustomSubtitlesClip
from customTextClip import CustomTextClip

fontsize = 50

video = VideoFileClip("files/garyvee.mp4")
width, height = video.size

shadow_dist = int(fontsize/10)

generator_shadow = lambda txt: CustomTextClip(txt, font='Boldfont-Bold', font_size=50, color='black', rotate = 10)
subtitles_shadow = CustomSubtitlesClip("files/garyvee.srt", generator_shadow).set_pos(("center", int(height*2/3) + shadow_dist))

generator = lambda txt: TextClip(txt, font='Boldfont-Bold', fontsize=50, color='white')
subtitles = CustomSubtitlesClip("files/garyvee.srt", generator)



shadow = CompositeVideoClip([video, subtitles_shadow])
result = CompositeVideoClip([shadow, subtitles.set_pos(("center", int(height*2/3)))])

result.write_videofile("files/beauty-garyvee.mp4", fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")