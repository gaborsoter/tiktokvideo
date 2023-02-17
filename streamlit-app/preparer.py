import re
import srt
import json

class Preparer:
    def __init__(self):
        return

    def __call__(self):
        with open("bits.txt") as file:
            bits = [line.rstrip() for line in file]

        f = open("caption.srt", "rt")
        subtitles = f.read()
        f.close()

        subs = list(srt.parse(subtitles))

        bitsubs = []

        bit_index = 1
        bit_start_time = subs[0].start
        added = True

        sub_index = 0

        bit_lengths = []
        total_bit_length = 0

        for bit in bits:
            length_of_bit = len(bit.split(" "))
            bit_lengths.append(total_bit_length)
            total_bit_length += length_of_bit

            bitsubs.append(srt.Subtitle(index=bit_index, start=subs[sub_index].start, 
                                        end=subs[sub_index + length_of_bit - 1].end, 
                                        content=bit, proprietary=''))

            sub_index += length_of_bit
            bit_index += 1
            
        CAPTION_FILE = open("input.srt", "w")
        CAPTION_FILE.write(srt.compose(bitsubs))
        CAPTION_FILE.close()

        with open('bit_lengths.txt', 'w') as filehandle:
            json.dump(bit_lengths, filehandle)

        f = open("input.srt", "rt")
        subtitles = f.read()
        f.close()

        subs = list(srt.parse(subtitles))

        # Exporting subtitle files
        for i in range(len(subs)):
            temp_sub = srt.Subtitle(index=1, start=subs[i].start, 
                                        end=subs[i].end, 
                                        content=subs[i].content.upper(), proprietary='')

            temp_sub = srt.compose([temp_sub])

            CAPTION_FILE = open("clips/clip_"+str(i)+".srt", "w")
            CAPTION_FILE.write(temp_sub)
            CAPTION_FILE.close()
