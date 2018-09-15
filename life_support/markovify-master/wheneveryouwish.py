import markovify
import nltk
import re
import csv

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def writeToCSV(sentences):
    with open('sentences.csv', 'w+') as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(sentences)

        
# Get raw text as string.
with open("../corpuses/ggia.txt") as f:
    ggia = f.read()
with open("../corpuses/horoscope.txt") as f:
    horoscope = f.read()
with open("../corpuses/oprah.txt") as f:
    oprah = f.read()
# with open("../corpuses/sugar.txt") as f:
#     sugar = f.read()

# Build the model.
# ggiaModel = markovify.Text(ggia)
# horoscopeModel = markovify.Text(horoscope)
# oprahModel = markovify.Text(oprah)
# sugarModel = markovify.Text(sugar)

ggiaNLTK = POSifiedText(ggia)
horoscopeNLTK = POSifiedText(horoscope)
oprahNLTK = POSifiedText(oprah)

comboModel = markovify.combine([ggiaNLTK, horoscopeNLTK, oprahNLTK], [2, 1, 1])

# for i in range(2):
#     print("\n"+comboModel.make_sentence()+"\n")

# Print three randomly-generated sentences of no more than 140 characters

sentences = []
for i in range(200):
    sentences.append(comboModel.make_short_sentence(200))

writeToCSV(sentences)
# print("\n"+comboModel.make_short_sentence(200)+"\n")
