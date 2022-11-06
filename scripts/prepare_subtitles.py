import re
import srt
from difflib import SequenceMatcher

with open("files/bits.txt") as file:
    bits = [line.rstrip() for line in file]

with open("files/transcript.txt") as file:
    transcript = [line.rstrip() for line in file]

f = open("files/subtitle.srt", "rt")
subtitles = f.read()
f.close()

tolerance = 0.8

def compare_strings(stringA, stringB):
    seq = SequenceMatcher(None, stringA.lower(), stringB.lower())
    return seq.ratio()

subs = list(srt.parse(subtitles))

bitsubs = []

bit_index = 1
bit_start_time = subs[0].start
added = True

sub_index = 0

for bit in bits:
    length_of_bit = len(bit.split(" "))

    bitsubs.append(srt.Subtitle(index=bit_index, start=subs[sub_index].start, 
                                end=subs[sub_index + length_of_bit - 1].end, 
                                content=bit, proprietary=''))

    sub_index += length_of_bit 
    bit_index += 1

CAPTION_FILE = open("files/garyvee.srt", "w")
CAPTION_FILE.write(srt.compose(bitsubs))
CAPTION_FILE.close()