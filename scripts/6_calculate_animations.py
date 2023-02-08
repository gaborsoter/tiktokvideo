import srt
import os
import openai
import json
from decouple import config
import unicodedata
import numpy as np

openai.api_key = config('OPENAI_API_KEY')

f = open("files/input.srt", "rt")
subtitles = f.read()
f.close()

subs = list(srt.parse(subtitles))

def find_probability(response):
    offsets = response["logprobs"]["text_offset"]
    count_logprobs = offsets.count(offsets[0])
    total_logprobs = 0
    for i in range(count_logprobs):
        total_logprobs += list(response["logprobs"]["top_logprobs"][i].values())[0]
    probability = 100*np.e**(total_logprobs)
    return probability

def find_emoji(subtitle):
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt="Find an emoji to the sentence.\n\nWelcome to Larry King Now: 👋\nour special guest is Gary Vaynerchuk: 👨\nThe self-proclaimed hustler: 🏃\nis a digital media mogul: 🎥\nauthor, web show host: ✍️\nand venture capitalist: 💵\nAs the CEO and: 👑\nNew York Times bestselling books: 📚\nHow did this all start?: 🤔\nI didn't know that:  😕\nand holds the number one: 🔝\nWhat happened with you?: 😯\nAsk Gary Vee,:  🙋\nHis newest book,:  📙\nrocket to the moon: 🚀\nThe hurricane came the next day: 🌪\n"+subtitle+":",
    temperature=0.8,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    logprobs=1,
    stop=["\n"]
    )
    
    return response["choices"][0]

emoji_array = []

for sub in subs:
    emoji_response = find_emoji(sub.content)
    probability = find_probability(emoji_response)

    a = emoji_response["text"]
    m = json.dumps({"k": a})
    emoji = str(json.loads(m)['k'].encode('raw_unicode_escape'))
    emoji_array.append([emoji, probability])

with open('files/emoji_array.txt', 'w') as file:
    for emoji in emoji_array:
        file.write('%s\n' % emoji)
