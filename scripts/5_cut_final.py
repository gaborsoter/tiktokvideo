# cut video
# python3 -m ffmpeg_smart_trim.trim files/output0.mp4 --start_time 00.000 --end_time 01.040 --output out0.mp4

# merge video
#ffmpeg -f concat -protocol_whitelist file,https,tcp,tls -safe 0 -i videos.txt -c copy output_final.mp4