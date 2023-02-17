import os
import openai
import numpy as np
from decouple import config

class Editor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.cuda.empty_cache()
        torch.random.manual_seed(0)
        return

    def __call__(self):
        f = open("transcript.txt", "rt")
        data = f.read()
        f.close()

        openai.api_key = config('OPENAI_API_KEY')

        print(data)

        data = data.replace('. ', '._END_')
        phrases = data.split('_END_')

        print(phrases)

        sentences = []

        for phrase in phrases:
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt="Split the sentences into smaller chunks such that the chunks don't have more than 6 words.\n\nInput: Welcome to Larry King Now. Our special guest is Gary Vaynerchuk. \n\n[\"Welcome to Larry King Now.\", \"Our special guest is Gary Vaynerchuk. \"]\n\nInput: The self-proclaimed hustler is a digital media mogul, author, web show host, and venture capitalist, among many other things.\n\n[\"The self-proclaimed hustler\", \"is a digital media mogul,\", \"author, web show host,\", \"and venture capitalist,\", \"among many other things.\"]\n\nInput: As the CEO and co-founder of VaynerMedia, Gary hosts the hugely popular YouTube show, Ask Gary Vee, and has penned three New York Times bestselling books.\n\n[\"As the CEO and\", \"co-founder of VaynerMedia,\", \"Gary hosts the hugely popular\", \"YouTube show, Ask Gary Vee,\", \"and has penned three\", \"New York Times bestselling books.\"]\n\nInput:" + phrase,
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )

            sentence = response["choices"][0]["text"].split("\n\n")
            sentence = [x for x in sentence if x != '']
            sentences.append(sentence)




        # Manipulating the GPT-3 output
        array = np.array(sentences).flatten()

        print(sentences)

        output = []
        for item in array:
            subitems = item.split('", "')
            for subitem in subitems:
                subitem = subitem.replace('["', '')
                subitem = subitem.replace('"]', '')
                output.append(subitem)

        with open('bits.txt', 'w') as filehandle:
            for listitem in output:
                filehandle.write('%s\n' % listitem)
