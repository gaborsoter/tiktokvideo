import ffmpeg

video = ffmpeg.input('files/input_wide.mp4')
audio_stream = ffmpeg.input('files/input_wide.mp4').audio

probe = ffmpeg.probe('files/input_wide.mp4')
video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]


width = int(video_streams[0]['width'])
height = int(video_streams[0]['height'])

new_width = int(height/16*9)
new_x_pos = int((width/2) - (new_width/2))

(
    ffmpeg
    .input('files/input_wide.mp4')
    .filter("crop", h=str(height), w=str(new_width), x=str(new_x_pos), y=str(0))
    .output(audio_stream, 'files/input.mp4')
    .run()
)
