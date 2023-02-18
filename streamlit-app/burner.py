import ffmpeg
import random
import os.path
import srt
from pathlib import Path
import streamlit as st


class Burner:
    def __init__(self):
        return

    def __call__(self):
        def calculate_font_size(value):
            # min and max character length
            leftMin = 0
            leftMax = 15

            # min and max font size
            rightMin = 40
            rightMax = 15

            leftSpan = leftMax - leftMin
            rightSpan = rightMax - rightMin

            # Convert the left range into a 0-1 range (float)
            valueScaled = float(value - leftMin) / float(leftSpan)

            # Convert the 0-1 range into a value in the right range.
            return int(rightMin + (valueScaled * rightSpan))

        def animate_subtitle(type, subtitle_path, current_bit_length, colour, font_size):
                f = open(subtitle_path, "rt")
                subtitle = f.read()
                f.close()
                subtitle = list(srt.parse(subtitle))

                if colour == "red":
                    subtitle_colour = "#D7090E"
                elif colour == "green":
                    subtitle_colour = "#36FE1E"
                elif colour == "biobubi":
                    subtitle_colour = "#4EABA4"
                else:
                    subtitle_colour = "#FAFF00"


                # Do nothing
                if type==-1:
                    temp_content = subtitle[0].content.split(" ")

                    division_point = int(len(temp_content)/2)
                    


                    temp_content.insert(division_point, "\n")
                    subtitle[0].content = '<font color="#FFFFFF" size="'+str(font_size)+'">' + ' '.join(temp_content[:division_point]) + " " + '</font>' + '<font color="#FFFFFF" size="'+str(font_size)+'">' + ' '.join(temp_content[division_point:]) + '</font>'
                    subtitle = srt.compose(subtitle)

                # Change colour for the whole subtitle
                if type==0:
                    temp_content = subtitle[0].content.split(" ")

                    division_point = int(len(temp_content)/2)
                    temp_content.insert(division_point, "\n")
                    subtitle[0].content = '<font color="#FAFF00" size="'+str(font_size)+'">' + ' '.join(temp_content[:division_point]) + " " + '</font>' + '<font color="#FAFF00" size="'+str(font_size)+'">' + ' '.join(temp_content[division_point:]) + '</font>'
                    subtitle = srt.compose(subtitle)

                # Change colour only for the second part of the subtitle
                if type==1:
                    temp_content = subtitle[0].content.split(" ")

                    division_point = int(len(temp_content)/2)
                    temp_content.insert(division_point, "\n")

                    subtitle[0].content = '<font color="#FFFFFF" size="'+str(font_size)+'">' + ' '.join(temp_content[:division_point]) + " " + '</font>' + '<font color="#FAFF00" size="'+str(font_size)+'">' + ' '.join(temp_content[division_point:]) + '</font>'
                    subtitle = srt.compose(subtitle)

                # Split the subtitle into words
                if type==2:
                    temp_content = subtitle[0].content.split(" ")
                    new_subtitles = []
                    for i in range(len(temp_content)):
                        content = caps[current_bit_length+i].content
                        font_size = calculate_font_size(len(content))
                        content = '<font color='+subtitle_colour+' size="'+str(font_size)+'">' + str(content) + '</font>'

                        print("CONTENT: ", content)
                        new_subtitles.append(srt.Subtitle(index=i+1, start=caps[current_bit_length+i].start, 
                                        end=caps[current_bit_length+i].end, 
                                        content=content, proprietary=''))

                    subtitle = srt.compose(new_subtitles)

                # Colour only the word that is spoken
                if type==3:

                    temp_content = subtitle[0].content.split(" ")
                    print("SUBTITLE: ", subtitle[0].content)
                    
                    new_subtitles = []
                    for i in range(len(temp_content)):
                        if i==0:
                            content = '<font color='+subtitle_colour+' size="'+str(font_size)+'">' + "".join(temp_content[i]) + " " + '</font>' + '<font color="#FFFFFF" size="'+str(font_size)+'">' + " ".join(temp_content[i+1:]) + '</font>'
                        elif i==(len(temp_content)-1):
                            content = '<font color="#FFFFFF" size="'+str(font_size)+'">' + " ".join(temp_content[:i]) + '</font>' + '<font color='+subtitle_colour+' size="'+str(font_size)+'">' + " " + "".join(temp_content[i]) + '</font>'
                        else:
                            content = '<font color="#FFFFFF" size="'+str(font_size)+'">' + " ".join(temp_content[:i]) + '</font>' + '<font color='+subtitle_colour+' size="'+str(font_size)+'">' + " " + "".join(temp_content[i]) + " " + '</font>' + '<font color="#FFFFFF" size="'+str(font_size)+'">' + " ".join(temp_content[i+1:]) + '</font>'
                        if (current_bit_length+i+1>(len(caps)-1)):
                            end = caps[current_bit_length+i].end
                        else:
                            end = caps[current_bit_length+i+1].start
                        new_subtitles.append(srt.Subtitle(index=i+1, start=caps[current_bit_length+i].start, 
                                        end=end, 
                                        content=content, proprietary=''))

                    subtitle = srt.compose(new_subtitles)
                    

                f = open(subtitle_path, "w")
                f.write(subtitle)
                f.close()

        video_path="input.mp4"
        audio = ffmpeg.input(video_path).audio

        path = Path('./input.mp4')

        st.write("isfile:", path.is_file())

        #fonts_dir = "/Users/gaborsoter/repos/tiktokvideo/scripts/files/gabor.otf"

        bit_lengths_file = open("bit_lengths.txt", "r")
        file_content = bit_lengths_file.read()
        bit_lengths_file.close()
        content_list = file_content.split(",")
        content_list[0] = content_list[0].replace('[', '')
        content_list[-1] = content_list[-1].replace(']', '')
        bit_lengths= [int(x) for x in content_list]

        f = open("caption.srt", "rt")
        captions = f.read()
        f.close()
        caps = list(srt.parse(captions))

        stream = ffmpeg.input(video_path)
        try:
            stream.output("input.mp4", vcodec="copy", acodec="copy").run(capture_stdout=True, capture_stderr=True)
            print("here")
        except ffmpeg.Error as e:
            print("here2")
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
            raise e


        angles = ["-10", "0", "10"]
        colour = ["red", "green", "yellow"]

        # concat subtitles

        i = 0
        '''
        while (os.path.exists("clip_"+str(i)+".srt")):
            subtitle_path = "clip_"+str(i)+".srt"
            #animation_type = random.randint(2, 3)
            animation_type = 3
            sub_colour = "yellow"
            fontsize = str(20)
            animate_subtitle(animation_type, subtitle_path, bit_lengths[i], sub_colour, fontsize)
            alignment = str(2)
            fontname = "Arial"
            outline = str(0)
            shadow = str(1)
            marginL = str(100)
            marginR = str(100)
            marginV = str(50)
            randomangle = random.randint(0, 2)
            angle = angles[randomangle]
            #angle = str(0)
            color = "80ff80"
            # FontName="+fontname+",
            style = "Alignment="+alignment+",Outline="+outline+",FontSize="+fontsize+",Shadow="+shadow+",MarginL="+marginL+",MarginR="+marginR+",MarginV="+marginV+",Angle="+angle+", PrimaryColour="+color
            #stream = ffmpeg.concat(stream.filter("subtitles", subtitle_path, force_style=style), audio, v=1, a=1)
            i += 1
            #fontsdir=fonts_dir,
            print("HERE")
            #stream.output("output.mp4").run(capture_stdout=True, capture_stderr=True)
        '''