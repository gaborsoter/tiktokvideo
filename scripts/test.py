import numpy as np

array = [['["Welcome to Larry King Now.", "Our special guest is Gary Vaynerchuk. "]'], ['["The self-proclaimed hustler", "is a digital media mogul,", "author, web show host,", "and venture capitalist,", "among many other things."]'], ['["As the CEO and", "co-founder of VaynerMedia,", "Gary hosts the hugely popular", "YouTube show, Ask Gary Vee,", "and has penned three", "New York Times bestselling books."]'], ['["Gary has been named to", "Fortune Magazine\'s 40 Under 40", "list of the most influential", "business leaders and holds", "the number one ranking on", "Forbes Top 40 Social Selling", "Market Masters.", "His newest book, Ask Gary Vee,", "is available now."]'], ['["How did this all start?", "Wine? What happened with you?"]'], ['["What happened with me is", "I had the great benefit of being an immigrant.", "I was born in Belarus in the former Soviet Union.", "My mother was from Belarus.", "I didn\'t know that.", "Minsk, I think.", "Yeah, I was born 40 minutes from Minsk."]']]

array = np.array(array).flatten()

output = []
for item in array:
    subitems = item.split('", "')
    for subitem in subitems:
        subitem = subitem.replace('["', '')
        subitem = subitem.replace('"]', '')
        output.append(subitem)