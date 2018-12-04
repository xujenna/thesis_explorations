import markovify
import nltk
import re
from nltk.stem import WordNetLemmatizer
import requests
import json
import random
from sklearn.externals import joblib
 

lemmatizer = WordNetLemmatizer()

# text_by_POS = {}
# text_by_POS['ADJ'] = []
# text_by_POS['ADV'] = []
# text_by_POS['NOUN'] = []
# text_by_POS['NUM'] = []
# text_by_POS['VERB'] = []
# text_by_POS['PREP'] = []


# class POSifiedText(markovify.Text):
#     def word_split(self, sentence):
#         words = re.split(self.word_split_pattern, sentence)
#         for tag in nltk.pos_tag(words):
#             if tag[1][:2] == 'JJ':
#                 text_by_POS['ADJ'].append(tag[0])
#             elif tag[1][:2] == 'RB':
#                 text_by_POS['ADV'].append(tag[0])
#             elif tag[1][:2] == 'NN':
#                 text_by_POS['NOUN'].append(tag[0])
#             elif tag[1][:2] == 'CD':
#                 text_by_POS['NUM'].append(tag[0])
#             elif tag[1][:2] == 'VB':
#                 text_by_POS['VERB'].append(lemmatizer.lemmatize(tag[0]))
#             elif tag[1][:2] == 'IN':
#                 text_by_POS['PREP'].append(tag[0])
#         return words


# POSifiedText(happyDB)


with open('happyDB_vocab.json', 'r') as f:
    text_by_POS = json.load(f)


url = "http://api.usno.navy.mil/rstt/oneday?date=11/12/2018&coords=40.7128N,74.0060W&tz=-5"
r = requests.get(url=url)
moonData = r.json()
moonFacillum = int(moonData['fracillum'][0:2])
# random.seed(moonFacillum)

adverb = text_by_POS['ADV'][random.randrange(0, len(text_by_POS['ADV']))]
verb = text_by_POS['VERB'][random.randrange(0, len(text_by_POS['VERB']))]
noun = text_by_POS['NOUN'][random.randrange(0, len(text_by_POS['NOUN']))]
preposition = text_by_POS['PREP'][random.randrange(0, len(text_by_POS['PREP']))]
noun2 = text_by_POS['NOUN'][random.randrange(0, len(text_by_POS['NOUN']))]

task = lemmatizer.lemmatize(verb) + " " + noun + " " + preposition + " " + noun2
print(task)
# with open("../corpuses/hm_only.txt") as f:
#     happyDB = f.read()

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        start = 0
        newWords = []
        for tag in nltk.pos_tag(words):
            if tag[1][:2] == "VB":
                start = 1
            if(start == 1):
                if(tag[1][:2] == 'VB'):
                    newWords.append(tuple((lemmatizer.lemmatize(tag[0]),tag[1])))
                elif(tag[1][:3] != "PRP"):
                    newWords.append(tag)
        print(newWords)
        POSwords = [ "::".join(tag) for tag in newWords ]
        return POSwords

    def word_join(self, POSwords):
        sentence = " ".join(word.split("::")[0] for word in POSwords)
        # print(sentence)
        return sentence

# happyMarkov = POSifiedText(happyDB)

# joblib.dump(happyMarkov, 'happyMarkov_Model.pkl')

# happyMarkov_Model = joblib.load('happyMarkov_Model.pkl')


# sentence = happyMarkov_Model.make_short_sentence(400)
# # print(sentence)
# sentence_POSified = POSifiedText(sentence)
# print(sentence_POSified)

# for tag in sentence_POSified:
#     print(tag)
# for i in range(20):
#     print("\n"+happyMarkov.make_sentence_with_start(verb)+"\n")