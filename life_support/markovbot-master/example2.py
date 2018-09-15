import os
import time
import csv

from markovbot import MarkovBot


# # # # #
# INITIALISE

# Initialise a MarkovBot instance
tweetbot = MarkovBot()
#
# with open('cleaned_hm.csv') as f:
#     reader = csv.reader(f)
#     next(reader,None)
#     data = [line for line in reader]
# with open('hm_only.txt', 'w+') as f:
#     writer = csv.writer(f)
#     for row in data:
#         writer.writerow([row[4]])
tweetbot.read("ggia.txt")


# # # # #
# TEXT GENERATION

# Generate text by using the generate_text method:
# 	The first argument is the length of your text, in number of words
# 	The 'seedword' argument allows you to feed the bot some words that it
# 	should attempt to use to start its text. It's nothing fancy: the bot will
# 	simply try the first, and move on to the next if he can't find something
# 	that works.
while True:
    my_first_text = tweetbot.generate_text(15)

    # Print your text to the console
    print(u'\ntweetbot says: "%s"' % (my_first_text))
    time.sleep(7)
